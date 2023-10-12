import json
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
import api.app_utils as app_utils
from .models import Todo, List

@api_view(['GET'])
def get_token(request):
    try:
        # For demo purposes the userId is hardcoded, 
        # In your app you'll fetch the user from the database 
        user_id = "4"
        token = app_utils.create_jwt_token(user_id)
        return JsonResponse({
            "token": token,
            "powersync_url": app_utils.power_sync_url
        }, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@api_view(['GET'])
def get_keys(request):
    try:
        return JsonResponse({
            "keys": [
                app_utils.power_sync_public_key_json
            ]
        }, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@api_view(['GET'])
def get_session(request):
    try:
        # For demo purposes the session is always valid,
        # In your app you'll need to handle user sessions 
        # and invalidate the session after expiry.
        return JsonResponse({
            "session": "valid"
        })
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
def auth(request):
    # For demo purposes the username and password are in plain text,
    # In your app you must handle usernames and passwords properly.
    data = json.loads(request.body.decode('utf-8'))
    username = data.get('username')
    password = data.get('password')
    user = User.objects.get(username=username, password=password)
    if user is not None:
        token = app_utils.create_jwt_token(user.id)
        response = {'access_token': token}
        return JsonResponse(response, status=200)
    else:
        return JsonResponse({'message': 'Authentication failed'}, status=401)

@api_view(['PUT', 'PATCH', 'DELETE'])
def upload_data(request):
    op = json.loads(request.body.decode('utf-8'))
    data = op.get('data')
    print(op)
    if op.get('table') == 'api_todo':
        if request.method == 'PUT':
            upsertTodo(data)
            return Response({'message': 'Todo updated'}, status=200)
        elif request.method == 'PATCH':
            updateTodo(data)
            return HttpResponse({'message': 'Todo updated'}, status=200)
        elif request.method == 'DELETE':
            try:
                todo = Todo.objects.get(id=data.get('id'))
                todo.delete()
                return HttpResponse({'message': 'Todo deleted'}, status=200)
            except Todo.DoesNotExist:
                return HttpResponse({'message': 'Todo does not exist'}, status=404)
    elif op.get('table') == 'api_list':
        if request.method == 'PUT':
            upsertList(data)
            return Response({'message': 'List created'}, status=200)
        elif request.method == 'PATCH':
            updateList(data)   
            return HttpResponse({'message': 'List updated'}, status=200)
        elif request.method == 'DELETE':
            try:
                list = List.objects.get(id=data.get('id'))
                list.delete()
                return HttpResponse({'message': 'List deleted'}, status=200)
            except List.DoesNotExist:
                return HttpResponse({'message': 'List does not exist'}, status=404)
                
def upsertTodo(data):
    try:
        todo = Todo.objects.get(id=data.get('id'))
        todo.description = data.get('description')
        todo.created_by = data.get('created_by')
        todo.list_id = data.get('list_id')
        todo.save()
    except Todo.DoesNotExist:
        todo = Todo(id=data.get('id'), description=data.get('description'), created_by=data.get('created_by'), list_id=data.get('list_id'))
        todo.save()

def updateTodo(data):
    todo = Todo.objects.get(id=data.get('id'))
    if todo is not None:
        todo.description = data.get('description')
        todo.created_by = data.get('created_by')
        todo.list_id = data.get('list_id')
        todo.save()

def upsertList(data):
    try:
        list = List.objects.get(id=data.get('id'))
        list.created_at = data.get('created_at')
        list.name = data.get('name')
        list.owner_id = data.get('owner_id')
        list.save()
        return Response({'message': 'List updated'}, status=200)
    except List.DoesNotExist:
        list = List(id=data.get('id'), created_at=data.get('created_at'), name=data.get('name'), owner_id=data.get('owner_id'))
        list.save()

def updateList(data):
    list = List.objects.get(id=data.get('id'))
    if list is not None:
        list.created_at = data.get('created_at')
        list.name = data.get('name')
        list.owner_id = data.get('owner_id')
        list.save()