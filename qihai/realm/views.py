from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse
from django.views import generic
from django.template import loader
from .models import User
from django.utils import timezone


def index(request):
    return HttpResponse('Hello Django.')


def users(request):
    us = User.objects.all()
    # users = []
    # for user in us:
    #     users.append(
    #         {'username': user.username, 'nickname': user.nickname, 'email': user.email}
    #     )
    return HttpResponse(us)


def uploadImage(request):
    if request.method == 'POST':
        pass
    # img = Img(img_url=request.FILES.get('img'))
    # img.save()
    # return render(request, 'imgUpload.html')
    return HttpResponse('ok')
