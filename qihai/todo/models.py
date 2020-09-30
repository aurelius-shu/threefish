from enum import Enum, unique
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


@unique
class ProjectType(Enum):
    undefined = 0
    learning = 1
    working = 2
    life = 3
    other = 4


@unique
class Status(Enum):
    doing = 1
    done = 2
    closed = 3


class Project(models.Model):
    name = models.CharField(max_length=30, default=' ')
    type = models.IntegerField(default=0, choices=[(tag.value, tag.name) for tag in ProjectType])
    status = models.IntegerField(default=1, choices=[(tag.value, tag.name) for tag in Status])
    owner = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='projects')
    create_time = models.DateTimeField(default=timezone.now)
    update_time = models.DateTimeField(auto_now=True)
    comment = models.CharField(max_length=255, default=' ')


class Task(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    keyword = models.CharField(max_length=30, default=' ')
    status = models.IntegerField(default=1, choices=[(tag.value, tag.name) for tag in Status])
    create_time = models.DateTimeField(default=timezone.now)
    update_time = models.DateTimeField(auto_now=True)
    description = models.CharField(max_length=255, default=' ')


class Schedule(models.Model):
    keyword = models.CharField(max_length=30, default=' ')
    status = models.IntegerField(default=1, choices=[(tag.value, tag.name) for tag in Status])
    create_time = models.DateTimeField(default=timezone.now)
    update_time = models.DateTimeField(auto_now=True)
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(default=timezone.now)
    comment = models.CharField(max_length=255, default=' ')


class Step(models.Model):
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE, related_name='steps')
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='steps')
    status = models.IntegerField(default=1, choices=[(tag.value, tag.name) for tag in Status])
    create_time = models.DateTimeField(default=timezone.now)
    update_time = models.DateTimeField(auto_now=True)
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(default=timezone.now)
    outcome = models.CharField(max_length=255, default=' ')
