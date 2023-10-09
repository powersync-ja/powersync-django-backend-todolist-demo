from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
import api.app_utils as app_utils

@api_view(['GET'])
def get_token(request):
    print("INCOMMING REQUEST [/get_token]", request)
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

@api_view(['POST'])
def auth(request):
    if request.method == 'POST':
        jwt = {}
    return JsonResponse(jwt)

@api_view(['PUT'])
def sync(request):
    # Implement your logic here
    return Response({"message": "PUT Sync endpoint"})

@api_view(['PATCH'])
def sync(request):
    # Implement your logic here
    return Response({"message": "PATCH Sync endpoint"})

@api_view(['DELETE'])
def sync(request):
    # Implement your logic here
    return Response({"message": "DELETE Sync endpoint"})