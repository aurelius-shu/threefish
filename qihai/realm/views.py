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
    # users = []
    # for user in us:
    #     users.append(
    #         {'username': user.username, 'nickname': user.nickname, 'email': user.email}
    #     )
    return HttpResponse(us)


@csrf_exempt
def upload_image(request):
    if request.method == 'POST' and request.FILES and request.FILES.keys():
        image_md5_key = request.POST['image_md5_key']
        if Image.objects.filter(md5_key=image_md5_key):
            return HttpResponse('existed.')

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
    return HttpResponse('ok')
