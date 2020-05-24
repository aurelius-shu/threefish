from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from .models import User, Image, Article
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
        us = User.objects.filter(username=username)
        # 如果已经存在，直接返回图片信息
        images = Image.objects.filter(md5_key=image_md5_key, upload_user=us[0])
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

    us = User.objects.filter(username=username)
    if not us:
        return HttpResponse(None)

    images = list(map(from_image_model, us[0].image_set.filter(is_deleted=False).order_by('-upload_time')))
    return HttpResponse(json.dumps(images))


@csrf_exempt
def remove_image(request, username, uid):
    """
    delete image
    :param request: http request
    :param username: username: str
    :param uid:
    :return:
    """

    us = User.objects.filter(username=username)
    if us:
        images = Image.objects.filter(upload_user=us[0], md5_key=uid)
        images.update(is_deleted=True)
    return HttpResponse('ok')


@csrf_exempt
def save_article(request, username):
    res = {}
    if request.method == 'POST':
        data = json.loads(request.body)
        author = User.objects.get(username=username)
        image = Image.objects.get(md5_key=data['image_md5_key'])
        # 如果已经存在该文章，更新
        if data['aid']:
            articles = Article.objects.filter(id=data['aid'], author=author)
            if articles:
                articles.update(title=data['title'], content=data['content'], image=image, update_time=timezone.now())
                res['is_succeed'] = True
                res['message'] = '文章已更新'
                res['aid'] = data['aid']
        # 如果不存在该文章，创建，保存
        else:
            article = Article(
                title=data['title'],
                author=author,
                content=data['content'],
                image=image,
                create_time=timezone.now(),
            )
            article.save()
            res['is_succeed'] = True
            res['message'] = '文章已创建'
            res['aid'] = article.pk

    return HttpResponse(json.dumps(res))


@csrf_exempt
def publish_article(request, username, aid):
    pass
