from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse
from django.views import generic
from django.template import loader
from .models import User, Image
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt


def index(request):
    return HttpResponse('<input accept="image/*,audio/*" type="file"/>')


def users(request):
    us = User.objects.all()
    return HttpResponse(us)


@csrf_exempt
def upload_image(request):
    """
    receive the uploading image
    save it to media/realm
    record in the table of realm_image
    :param request: http request
    :return: image：Image
    """

    if request.method == 'POST' and request.FILES and request.FILES.keys():
        image_md5_key = request.POST['image_md5_key']
        # 如果已经存在，直接返回图片信息
        images = Image.objects.filter(md5_key=image_md5_key)
        if images:
            return HttpResponse(images[0])

        upload_user = request.POST['upload_user']
        us = User.objects.filter(username=upload_user)

        image_resource = request.FILES.get('file')

        image = Image(
            md5_key=image_md5_key,
            filename=image_resource.name,
            upload_user=us[0] if us else None,
            upload_time=timezone.now(),
            url=image_resource
        )
        image.save()
    return HttpResponse(image)


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

    return HttpResponse(us[0].image_set.all().order_by('-upload_time')[:5])
