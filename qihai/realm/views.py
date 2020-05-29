from django.http import HttpResponse, Http404
from .models import User, Image, Column, Article, ArticleStatus
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
import json
from datetime import datetime


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
def manage_articles(request, username):
    """

    :param request:
    :param username:
    :return:
    """
    from .core.article import create_article
    data = json.loads(request.body)
    article_id = create_article(
        username,
        data['image_md5_key'],
        data['title'],
        data['content'],
    )
    return HttpResponse(article_id)


@csrf_exempt
def manage_article_edit(request, article_id):
    pass


@csrf_exempt
def manage_article_update(request, article_id):
    pass


@csrf_exempt
def manage_article_remove(request, article_id):
    pass


@csrf_exempt
def manage_article_publish(request, article_id):
    pass


@csrf_exempt
def manage_articles(request, username):
    """
    save article in dbms
    :param request: http request
    :param username: username: str
    :return:
    """

    res = {}
    data = json.loads(request.body)
    author = User.objects.get(username=username)
    image = Image.objects.get(md5_key=data['image_md5_key'])
    # 如果已经存在该文章，更新
    aid = int(data['aid'])
    if aid > 0:
        articles = Article.objects.filter(id=aid, author=author)
        if articles and len(articles) > 0:
            articles.update(title=data['title'])
            articles.update(content=data['content'])
            articles.update(image=image)
            articles.update(update_time=timezone.now())
            res['is_succeed'] = True
            res['message'] = '文章已更新'
            res['aid'] = data['aid']
    # 如果不存在该文章，创建，保存
    if aid < 1 or not articles or len(articles) < 1:
        article = Article(
            title=data['title'],
            author=author,
            content=data['content'],
            image=image,
            create_time=timezone.now(),
        )
        article.save()
        res['is_succeed'] = True
        res['message'] = '文章保存成功'
        res['aid'] = article.pk

    return HttpResponse(json.dumps(res))


@csrf_exempt
def publish_article(request, username, aid):
    """
    publish article
    :param request: http request
    :param username: username: str
    :param aid: article id: Article.pk
    :return:
    """

    res = {}
    author = User.objects.get(username=username)
    articles = Article.objects.filter(id=aid, author=author)
    if articles:
        articles.update(status=ArticleStatus.Published.value)
        articles.update(publish_time=timezone.now())
        res['is_succeed'] = True
        res['message'] = '文章发布成功'
        res['aid'] = articles[0].pk
    else:
        res['is_succeed'] = False
        res['message'] = '文章不存在'
        res['aid'] = aid
    return HttpResponse(json.dumps(res))


@csrf_exempt
def article_detail(request, username, aid):
    """
    article details
    :param request: http request
    :param username:  username: str
    :param aid: article id: Article.pk
    :return:
    """

    author = User.objects.get(username=username)
    article = Article.objects.get(id=aid, author=author)
    res = {
        'is_succeed': True,
        'message': '',
        'data': {
            'create_time': datetime.strftime(article.create_time, '%Y-%m-%d %H:%M:%S'),
            'title': article.title,
            'image': article.image.url.url,
            'content': article.content,
        }
    }
    return HttpResponse(json.dumps(res))
