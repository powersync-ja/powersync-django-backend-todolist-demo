from django.urls import path
from . import views

urlpatterns = [
    path('get_powersync_token/', views.get_powersync_token,
         name='get_powersync_token'),
    path('get_keys/', views.get_keys, name='get_keys'),
    path('get_session/', views.get_session, name='get_session'),
    path('auth/', views.auth, name='auth'),
    path('register/', views.register, name='register'),
    path('upload_data/', views.upload_data, name='upload_data'),
]
