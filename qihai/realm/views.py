from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse
from django.views import generic
from django.template import loader
from .models import User, Image
from django.utils import timezone


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


from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def uploadImage(request):
    if request.method == 'POST':
        image_inm = request.FILES.get('file')
        if image_inm:
            image = Image(filename=image_inm.name, upload_time=timezone.now(), img_url=image_inm)
            image.save()
    return HttpResponse('ok')
