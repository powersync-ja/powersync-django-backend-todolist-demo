from django.urls import path
from . import views

urlpatterns = [
    path('get_token/', views.get_token, name='get_token'),
    path('get_keys/', views.get_keys, name='get_keys'),
    path('get_session/', views.get_session, name='get_session'),
    path('auth/', views.auth, name='auth'),
    path('sync/', views.sync, name='sync'),
]