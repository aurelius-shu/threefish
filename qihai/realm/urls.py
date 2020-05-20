from django.urls import path
from . import views

app_name = 'realm'
urlpatterns = [
    path('', views.index, name='index'),
    path('users/', views.users, name='users'),
    path('upload/image', views.uploadImage, name='uploadImage'),
]
