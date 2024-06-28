import json
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
import api.app_utils as app_utils
from .models import Todos, Lists

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
    try: 
        user = authenticate(username=username, password=password)
        if user is not None:
            token = app_utils.create_jwt_token(user.id)
            response = {'access_token': token}
            return JsonResponse(response, status=200)
        else:
            logger.warning(f"Authentication failed for username: {username}")
            return JsonResponse({'message': 'Authentication failed'}, status=401)

    except json.JSONDecodeError as e:
        logger.error(f"JSON decode error: {e}")
        return JsonResponse({'message': 'Invalid JSON'}, status=400)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return JsonResponse({'message': 'Internal server error'}, status=500)

@api_view(['PUT', 'PATCH', 'DELETE'])
def upload_data(request):
    op = json.loads(request.body.decode('utf-8'))
    data = op.get('data')
    print(op)
    if op.get('table') == 'todos':
        if request.method == 'PUT':
            upsertTodo(data)
            return Response({'message': 'Todo updated'}, status=200)
        elif request.method == 'PATCH':
            updateTodo(data)
            return HttpResponse({'message': 'Todo updated'}, status=200)
        elif request.method == 'DELETE':
            try:
                todo = Todos.objects.get(id=data.get('id'))
                todo.delete()
                return HttpResponse({'message': 'Todo deleted'}, status=200)
            except Todos.DoesNotExist:
                return HttpResponse({'message': 'Todo does not exist'}, status=404)
    elif op.get('table') == 'lists':
        if request.method == 'PUT':
            upsertList(data)
            return Response({'message': 'List created'}, status=200)
        elif request.method == 'PATCH':
            updateList(data)   
            return HttpResponse({'message': 'List updated'}, status=200)
        elif request.method == 'DELETE':
            try:
                list = Lists.objects.get(id=data.get('id'))
                list.delete()
                return HttpResponse({'message': 'List deleted'}, status=200)
            except Lists.DoesNotExist:
                return HttpResponse({'message': 'List does not exist'}, status=404)
                
def upsertTodo(data):
    try:
        todo = Todos.objects.get(id=data.get('id'))
        todo.description = data.get('description')
        todo.created_by = data.get('created_by')
        todo.list_id = data.get('list_id')
        todo.save()
    except Todos.DoesNotExist:
        todo = Todos(id=data.get('id'), description=data.get('description'), created_by=data.get('created_by'), list_id=data.get('list_id'))
        todo.save()

def updateTodo(data):
    todo = Todos.objects.get(id=data.get('id'))
    if todo is not None:
        if 'description' in data:
            todo.description = data.get('description')
        if 'created_by' in data:
            todo.created_by = data.get('created_by')
        if 'list_id' in data:
            todo.list_id = data.get('list_id')
        if 'completed' in data:
            todo.completed = data.get('completed')
        if 'completed_by' in data:
            todo.completed_by = data.get('completed_by')
        if 'completed_at' in data:
            todo.completed_at = data.get('completed_at')
        todo.save()

def upsertList(data):
    try:
        list = Lists.objects.get(id=data.get('id'))
        list.created_at = data.get('created_at')
        list.name = data.get('name')
        list.owner_id = data.get('owner_id')
        list.save()
        return Response({'message': 'List updated'}, status=200)
    except Lists.DoesNotExist:
        list = Lists(id=data.get('id'), created_at=data.get('created_at'), name=data.get('name'), owner_id=data.get('owner_id'))
        list.save()

def updateList(data):
    list = Lists.objects.get(id=data.get('id'))
    if list is not None:
        list.created_at = data.get('created_at')
        list.name = data.get('name')
        list.owner_id = data.get('owner_id')
        list.save()