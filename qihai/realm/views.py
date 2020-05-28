from django.http import HttpResponse, Http404
from .models import User, Image, Column, Article, ArticleStatus
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
import json
from datetime import datetime


@csrf_exempt
def admin_users(request, page_index):
    """
    list users
    :param request:
    :param page_index:
    :return:
    """
    from .core.user import get_users_page
    users_page = get_users_page(page_index=page_index)
    return HttpResponse(json.dumps(users_page))


@csrf_exempt
def manage_images(request, username):
    """
    list images - get
    upload images - post
    :param request:
    :param username:
    :return:
    """
    # list
    if request.method == 'GET':
        from .core.image import get_images_by_user
        images = get_images_by_user(username)
        return HttpResponse(json.dumps(images))

    # upload
    if request.method == 'POST':
        from .core.image import upload_image
        res = upload_image(request, username)
        return HttpResponse(json.dumps(res))

    raise Http404


@csrf_exempt
def manage_images_remove(request, username, image_md5_key):
    """

    :param request:
    :param username:
    :param image_md5_key:
    :return:
    """
    from .core.image import remove_image
    res = remove_image(username, image_md5_key)
    return HttpResponse(res)


@csrf_exempt
def columns(request, username):
    from .core.column import get_columns
    cls = get_columns(username)
    return HttpResponse(json.dumps(cls))


###### 写到这里了 ######

@csrf_exempt
def save_article(request, username):
    """
    save article in dbms
    :param request: http request
    :param username: username: str
    :return:
    """

    res = {}
    data = json.loads(request.body)
    author = User.objects.get(username=username)
    image = Image.objects.get(md5_key=data['image_md5_key'])
    # 如果已经存在该文章，更新
    aid = int(data['aid'])
    if aid > 0:
        articles = Article.objects.filter(id=aid, author=author)
        if articles and len(articles) > 0:
            articles.update(title=data['title'])
            articles.update(content=data['content'])
            articles.update(image=image)
            articles.update(update_time=timezone.now())
            res['is_succeed'] = True
            res['message'] = '文章已更新'
            res['aid'] = data['aid']
    # 如果不存在该文章，创建，保存
    if aid < 1 or not articles or len(articles) < 1:
        article = Article(
            title=data['title'],
            author=author,
            content=data['content'],
            image=image,
            create_time=timezone.now(),
        )
        article.save()
        res['is_succeed'] = True
        res['message'] = '文章保存成功'
        res['aid'] = article.pk

    return HttpResponse(json.dumps(res))


@csrf_exempt
def publish_article(request, username, aid):
    """
    publish article
    :param request: http request
    :param username: username: str
    :param aid: article id: Article.pk
    :return:
    """

    res = {}
    author = User.objects.get(username=username)
    articles = Article.objects.filter(id=aid, author=author)
    if articles:
        articles.update(status=ArticleStatus.Published.value)
        articles.update(publish_time=timezone.now())
        res['is_succeed'] = True
        res['message'] = '文章发布成功'
        res['aid'] = articles[0].pk
    else:
        res['is_succeed'] = False
        res['message'] = '文章不存在'
        res['aid'] = aid
    return HttpResponse(json.dumps(res))


@csrf_exempt
def article_detail(request, username, aid):
    """
    article details
    :param request: http request
    :param username:  username: str
    :param aid: article id: Article.pk
    :return:
    """

    author = User.objects.get(username=username)
    article = Article.objects.get(id=aid, author=author)
    res = {
        'is_succeed': True,
        'message': '',
        'data': {
            'create_time': datetime.strftime(article.create_time, '%Y-%m-%d %H:%M:%S'),
            'title': article.title,
            'image': article.image.url.url,
            'content': article.content,
        }
    }
    return HttpResponse(json.dumps(res))


@csrf_exempt
def query_articles_by_column(request, username, cid):
    author = User.objects.get(username=username)
    if cid:
        arts = Article.objects.filter(author=author, column=cid, status=ArticleStatus.Published.value). \
            order_by('-publish_time')
    else:
        arts = Article.objects.filter(author=author, status=ArticleStatus.Published.value). \
            order_by('-publish_time')
    res = list(map(lambda article: {
        'id': article.pk,
        'title': article.title,
        'comment': article.comment,
        'publish_time': datetime.strftime(article.publish_time, '%Y-%m-%d %H:%M:%S'),
        'update_time': datetime.strftime(article.update_time, '%Y-%m-%d %H:%M:%S'),
        'column': article.column.name,
        'image': article.image.url.url
    }, arts))
    return HttpResponse(json.dumps(res))
