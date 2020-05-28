from django.urls import path
from . import views

app_name = 'realm'
urlpatterns = [
    path('', views.index),
    path('users', views.users),

    # column
    # list
    path('<str:username>/columns', views.columns),
    # articles
    path('<str:username>/columns/<int:cid>/articles', views.query_articles_by_column),

    # article
    # list page - get
    path('<str:username>/articles', views.list_or_create_articles),
    # get - get ;
    path('<str:username>/articles/<int:aid>', views.get_or_update_article),

    # manage
    # article
    # list page - get
    path('<str:username>/manage/articles/<int:pid>', views.manage_articles_list),
    # create - post
    path('<str:username>/manage/articles', views.manage_articles),
    # edit - post
    path('<str:username>/manage/articles/<int:aid>/edit', views.manage_article_edit),
    # update - post
    path('<str:username>/manage/articles/<int:aid>/update', views.manage_article_update),
    # remove - post
    path('<str:username>/manage/articles/<int:aid>/remove', views.manage_article_remove),
    # publish - post
    path('<str:username>/manage/articles/<int:aid>/publish', views.manage_article_publish),

    # image
    # list - get;
    path('<str:username>/manage/images', views.manage_images),
    # post - upload
    path('<str:username>/manage/images', views.manage_images),
    # remove
    path('<str:username>/manage/images/<str:image_md5_key>/remove', views.manage_images_remove),
]
