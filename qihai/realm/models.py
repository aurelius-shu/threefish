from django.db import models


class User(models.Model):

    def __str__(self):
        return (self.nickname or self.username) + (('<%s>' % self.email) if self.email else '')

    username = models.CharField(max_length=200)
    nickname = models.CharField(max_length=200)
    phone = models.CharField(max_length=13)
    email = models.CharField(max_length=30)
    password = models.CharField(max_length=128)
    reg_time = models.DateTimeField('time registered')
    last_login = models.DateTimeField('time last login')
    status = models.BooleanField('active or inactive')
