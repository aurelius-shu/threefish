from django.db import models
from django.utils import timezone
from enum import Enum, unique


@unique
class ArticleStatus(Enum):
    Saved = 1
    Published = 2
    Removed = 3


class User(models.Model):
    """
    user = User(
        username='aurelius',
        nickname='三只鱼',
        phone='13168096934',
        email='aurelius-shu@qq.com',
        password='models.CharField(max_length=128)',
        reg_time=timezone.now(),
        last_login=timezone.now(),
        is_active=True,
    )
    """

    def __str__(self):
        return (self.nickname or self.username) + (('<%s>' % self.email) if self.email else '')

    username = models.CharField(max_length=200)
    nickname = models.CharField(max_length=200)
    avatar = models.ForeignKey(to='Image', blank=True, null=True, on_delete=models.SET_NULL)
    phone = models.CharField(max_length=13)
    email = models.CharField(max_length=30)
    password = models.CharField(max_length=128)
    reg_time = models.DateTimeField('time registered')
    last_login = models.DateTimeField('time last login')
    is_active = models.BooleanField('active or inactive')


class Image(models.Model):
    """
    图片资源
    """

    def __str__(self):
        return '<%s>%s' % (self.upload_time, self.filename)

    md5_key = models.CharField(max_length=36, default=' ')
    filename = models.CharField(max_length=200, default=' ')
    upload_user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    upload_time = models.DateTimeField('time upload')
    # 指定图片上传路径，即media/realm/
    image = models.ImageField(upload_to='realm/', blank=True, null=True)
    is_deleted = models.BooleanField('is deleted', default=False)


class Column(models.Model):
    """
    栏目
    """

    name = models.CharField(max_length=10)
    comment = models.CharField(max_length=255)
    author = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    create_time = models.DateTimeField('time created', default=timezone.now)
    update_time = models.DateTimeField('time updated', default=timezone.now)
    is_delete = models.BooleanField('is deleted', default=False)


class Article(models.Model):
    """
    文章
    """

    def __str__(self):
        return '<%s>%s' % (self.publish_time, self.title)

    title = models.CharField(max_length=100)
    column = models.ForeignKey(Column, blank=True, null=True, on_delete=models.SET_NULL)
    author = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    card = models.ForeignKey(Image, blank=True, null=True, on_delete=models.SET_NULL)
    comment = models.CharField(max_length=255)
    status = models.IntegerField(choices=[(tag.value, tag.name) for tag in ArticleStatus],
                                 default=ArticleStatus.Saved.value)
    create_time = models.DateTimeField('time created', default=timezone.now)
    update_time = models.DateTimeField('time updated', default=timezone.now)
    publish_time = models.DateTimeField('time published', blank=True, null=True)
    content = models.TextField()
