import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
import api.app_utils as app_utils
from .models import Todo

@api_view(['GET'])
def get_token(request):
    try:
        user_id = "akfnnasdfnpp"
        token = app_utils.create_jwt_token(user_id)
        return JsonResponse({
            "token": token,
            "powersync_url": app_utils.power_sync_url
        })
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@api_view(['GET'])
def get_keys(request):
    try:
        return JsonResponse({
            "keys": [
                app_utils.power_sync_private_key_json
            ]
        })
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@api_view(['GET'])
def get_session(request):
    try:
        return JsonResponse({
            "session": "valid"
        })
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
def auth(request):
    data = json.loads(request.body.decode('utf-8'))
    username = data.get('username')
    password = data.get('password')
    user = User.objects.get(username=username, password=password)
    if user is not None:
        token = app_utils.create_jwt_token(user.id)
        session = login(request, user)
        print(session)
        resonse = {'access_token': token}
        print(resonse)
        return JsonResponse(resonse)
    else:
        return JsonResponse({'message': 'Authentication failed'}, status=401)

@api_view(['PUT'])
def sync(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        # Attempt to retrieve an existing Todo object with the given todo_id
        todo = Todo.objects.get(id=data.get('id'))
        # If the Todo object exists, update its fields
        todo.description = data.get('description')
        todo.created_by = data.get('created_by')
        todo.list_id = data.get('list_id')
        todo.save()
        return JsonResponse({'message': 'Todo updated'}, status=200)
    except Todo.DoesNotExist:
        # If the Todo object does not exist, create a new one
        todo = Todo(id=data.get('id'), description=data.get('description'), created_by=data.get('created_by'), list_id=data.get('list_id'))
        todo.save()
        return JsonResponse({'message': 'Todo created'}, status=200)

@api_view(['PATCH'])
def sync(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        # Attempt to retrieve an existing Todo object with the given todo_id
        todo = Todo.objects.get(id=data.get('id'))
        if todo is not None:
            # If the Todo object exists, update its fields
            todo.description = data.get('description')
            todo.created_by = data.get('created_by')
            todo.list_id = data.get('list_id')
            todo.save()
            return JsonResponse({'message': 'Todo updated'}, status=200)
    except Todo.DoesNotExist:
        return JsonResponse({'message': 'Todo does not exist'}, status=404)

@api_view(['DELETE'])
def sync(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        # Attempt to retrieve the Todo object by its id
        todo = Todo.objects.get(id=data.get('id'))
        todo.delete()
        return JsonResponse({'message': 'Todo deleted'}, status=200)
    except Todo.DoesNotExist:
       return JsonResponse({'message': 'Todo does not exist'}, status=404)