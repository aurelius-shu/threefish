from django.urls import path
from . import views

app_name = 'realm'
urlpatterns = [
    path('', views.index, name='index'),
    path('users/', views.users, name='users'),
    path('<str:username>/images', views.query_images, name='queryImages'),
    path('<str:username>/images/upload', views.upload_image, name='uploadImage'),
    path('<str:username>/images/remove/<str:uid>', views.remove_image, name='removeImage'),
    path('<str:username>/articles/save', views.save_article, name='saveArticle'),
    path('<str:username>/articles/publish/<str:aid>', views.publish_article, name='publishArticle'),
]
