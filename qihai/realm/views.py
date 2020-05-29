from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt
import json


@csrf_exempt
def admin_users(request, page_index):
    """
    list users
    :param request:
    :param page_index:
    :return:
    """
    from .core.user import get_users_page
    users_page = get_users_page(page_index=page_index)
    return HttpResponse(json.dumps(users_page))


@csrf_exempt
def columns(request, username):
    """

    :param request:
    :param username:
    :return:
    """
    from .core.column import get_columns
    cls = get_columns(username)
    return HttpResponse(json.dumps(cls))


@csrf_exempt
def get_article_page_by_column(request, username, column_id, page_index):
    """

    :param request:
    :param username:
    :param column_id:
    :param page_index:
    :return:
    """
    from .core.article import get_article_page_by_column
    article_page = get_article_page_by_column(username, column_id, page_index)
    return HttpResponse(json.dumps(article_page))


@csrf_exempt
def get_article(request, username, article_id):
    """

    :param request:
    :param username:
    :param article_id:
    :return:
    """
    from .core.article import get_article
    article = get_article(username, article_id)
    return HttpResponse(json.dumps(article))


@csrf_exempt
def manage_images(request, username):
    """
    list images - get
    upload images - post
    :param request:
    :param username:
    :return:
    """
    # list
    if request.method == 'GET':
        from .core.image import get_images_by_user
        images = get_images_by_user(username)
        return HttpResponse(json.dumps(images))

    # upload
    if request.method == 'POST':
        from .core.image import upload_image
        res = upload_image(request, username)
        return HttpResponse(json.dumps(res))

    raise Http404


@csrf_exempt
def manage_images_remove(request, username, image_md5_key):
    """

    :param request:
    :param username:
    :param image_md5_key:
    :return:
    """
    from .core.image import remove_image
    res = remove_image(username, image_md5_key)
    return HttpResponse(res)


@csrf_exempt
def manage_get_article_page(request, username, page_index):
    """

    :param request:
    :param username:
    :param page_index:
    :return:
    """
    from .core.article import get_articles
    article_page = get_articles(username, page_index)
    return HttpResponse(json.dumps(article_page))


@csrf_exempt
def manage_articles_create(request, username):
    """

    :param request:
    :param username:
    :return:
    """
    from .core.article import create_article
    data = json.loads(request.body)
    article_id = create_article(
        username,
        data['title'],
        data['column_id'],
        data['image_md5_key'],
        data['comment'],
        data['content'],
    )
    return HttpResponse(article_id)


@csrf_exempt
def manage_articles_edit(request, username, article_id):
    """

    :param request:
    :param username:
    :param article_id:
    :return:
    """
    from .core.article import edit_article
    article = edit_article(username, article_id)
    return HttpResponse(json.dumps(article))


@csrf_exempt
def manage_articles_update(request, username, article_id):
    """

    :param request:
    :param username:
    :param article_id:
    :return:
    """
    from .core.article import update_article
    res = update_article(username, article_id, json.loads(request.body))
    return HttpResponse(json.dumps(res))


@csrf_exempt
def manage_articles_remove(request, username, article_id):
    """

    :param request:
    :param username:
    :param article_id:
    :return:
    """
    from .core.article import remove_article
    res = remove_article(username, article_id)
    return HttpResponse(json.dumps(res))


@csrf_exempt
def manage_articles_publish(request, username, article_id):
    """

    :param request:
    :param username:
    :param article_id:
    :return:
    """
    from .core.article import publish_article
    res = publish_article(username, article_id)
    return HttpResponse(json.dumps(res))
