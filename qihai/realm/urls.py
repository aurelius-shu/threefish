from django.urls import path
from . import views

app_name = 'realm'
urlpatterns = [
    # user
    # register - post
    path('register', views.register),
    # signin - post
    path('signin', views.signin),
    # signout - post
    path('signout', views.signout),

    # admin
    # list user - get
    path('admin/users/<int:page_index>', views.admin_users),

    # column
    # list - get
    path('<str:username>/columns', views.columns),
    # article page - get
    path('<str:username>/columns/<int:column_id>/articles/<int:page_index>', views.get_article_page_by_column),

    # article
    # get - get ;
    path('<str:username>/articles/<int:article_id>', views.get_article),

    # manage

    # image
    # list - get;
    # upload - post
    path('<str:username>/manage/images', views.manage_images),
    # remove
    path('<str:username>/manage/images/<str:image_md5_key>/remove', views.manage_images_remove),

    # article
    # list page - get
    path('<str:username>/manage/articles/<int:page_index>', views.manage_get_article_page),
    # create - post
    path('<str:username>/manage/articles', views.manage_articles_create),
    # edit - post
    path('<str:username>/manage/articles/<int:article_id>/edit', views.manage_articles_edit),
    # update - post
    path('<str:username>/manage/articles/<int:article_id>/update', views.manage_articles_update),
    # remove - post
    path('<str:username>/manage/articles/<int:article_id>/remove', views.manage_articles_remove),
    # publish - post
    path('<str:username>/manage/articles/<int:article_id>/publish', views.manage_articles_publish),
]
