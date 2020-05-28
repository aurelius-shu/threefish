from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from .models import User, Image, Column, Article, ArticleStatus
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
import json
from datetime import datetime


def from_image_model(image):
    """
    build image info from `Image` Model
    :param image: `Image` Model
    :return: image info
    """
    return {
        'uid': image.md5_key,
        'name': image.filename,
        'url': image.url.url,
        'upload_time': datetime.strftime(image.upload_time, '%Y-%m-%d %H:%M:%S')
    }


def index(request):
    return HttpResponse('Realm Index')


def users(request):
    us = User.objects.all()
    return HttpResponse(us)


@csrf_exempt
def upload_image(request, username):
    """
    receive the uploading image
    save it to media/realm
    record in the table of realm_image
    :param request: http request
    :param username:
    :return: image：Image
    """

    res = {}
    if request.method == 'POST' and request.FILES and request.FILES.keys():
        image_md5_key = request.POST['image_md5_key']
        user = User.objects.get(username=username)
        # 如果已经存在，直接返回图片信息
        images = Image.objects.filter(md5_key=image_md5_key, upload_user=user)
        if images:
            image = images[0]
            if image.is_deleted:
                images.update(is_deleted=False)
                res['message'] = '图片上传成功'
                res['is_succeed'] = True
            else:
                res['message'] = '图片已经上传'
                res['is_succeed'] = False
            res['image'] = from_image_model(image)
        else:
            image_resource = request.FILES.get('file')
            image_name = image_resource.name
            image_resource.name = image_md5_key + '.' + image_name.split('.')[-1]
            image = Image(
                md5_key=image_md5_key,
                filename=image_name,
                upload_user=us[0] if us else None,
                upload_time=timezone.now(),
                url=image_resource
            )
            image.save()
            res['message'] = '图片上传成功'
            res['is_succeed'] = True
            res['image'] = from_image_model(image)

    return HttpResponse(json.dumps(res))


@csrf_exempt
def query_images(request, username):
    """
    query images where `username` uploaded
    :param request: http request
    :param username: user who uploaded
    :return: images: list<Image>
    """

    user = User.objects.get(username=username)
    images = list(map(from_image_model, user.image_set.filter(is_deleted=False).order_by('-upload_time')))
    return HttpResponse(json.dumps(images))


@csrf_exempt
def remove_image(request, username, image_md5_key):
    """
    delete image
    :param request: http request
    :param username: username: str
    :param image_md5_key: Image.md5_key
    :return:
    """

    user = User.objects.get(username=username)
    images = Image.objects.filter(upload_user=user, md5_key=image_md5_key)
    images.update(is_deleted=True)
    return HttpResponse('ok')


@csrf_exempt
def columns(request, username):
    cols = Column.objects.all().order_by('-update_time')[:6]
    res = list(map(lambda column: {'id': column.pk, 'name': column.name}, cols))
    return HttpResponse(json.dumps(res))


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
