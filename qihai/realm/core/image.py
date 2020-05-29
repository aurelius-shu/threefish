from qihai.realm.models import User, Image
from django.shortcuts import get_object_or_404
from datetime import datetime
from django.utils import timezone


def read_image(image):
    """
    build image info from `Image` Model
    :param image: `Image` Model
    :return: image info
    """
    return {
        'id': image.pk,
        'md5_key': image.md5_key,
        'filename': image.filename,
        'upload_user': image.upload_user,
        'upload_time': datetime.strftime(image.upload_time, '%Y-%m-%d %H:%M:%S'),
        'image_url': image.image.url,
        'is_deleted': image.is_deleted,
    }


def get_images_by_user(username):
    """

    :param username:
    :return:
    """

    user = get_object_or_404(User, username=username)
    images = list(map(read_image, user.image_set.filter(is_deleted=False).order_by('-upload_time')))
    return images


def upload_image(request, username):
    """

    :param request:
    :param username:
    :return:
    """
    res = {}
    md5_key = request.POST['image_md5_key']
    user = User.objects.get(username=username)
    # 如果已经存在，直接返回图片信息
    images = Image.objects.filter(md5_key=md5_key, upload_user=user)
    if images and images.count():
        image = images[0]
        if image.is_deleted:
            images.update(is_deleted=False)
            res['message'] = '图片上传成功'
            res['is_succeed'] = True
        else:
            res['message'] = '图片已经上传'
            res['is_succeed'] = False
    else:
        image_file = request.FILES.get('file')
        image_name = image_file.name
        image_file.name = md5_key + '.' + image_name.split('.')[-1]
        image = Image(
            md5_key=md5_key,
            filename=image_name,
            upload_user=user,
            upload_time=timezone.now(),
            image=image_file
        )
        image.save()
        res['message'] = '图片上传成功'
        res['is_succeed'] = True

    res['image'] = read_image(image)
    return res


def remove_image(username, image_md5_key):
    """

    :param username:
    :param image_md5_key:
    :return:
    """
    user = get_object_or_404(User, username=username)
    images = Image.objects.filter(upload_user=user, md5_key=image_md5_key)
    images.update(is_deleted=True)
    return True
