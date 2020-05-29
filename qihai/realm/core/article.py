from django.shortcuts import get_object_or_404
from qihai.realm.models import User, Column, ArticleStatus, Image, Article
from datetime import datetime
from django.utils import timezone


def read_article(article):
    """

    :param article:
    :return:
    """
    return {
        'id': article.pk,
        'title': article.title,
        'comment': article.comment,
        'publish_time': datetime.strftime(article.publish_time, '%Y-%m-%d %H:%M:%S'),
        'update_time': datetime.strftime(article.update_time, '%Y-%m-%d %H:%M:%S'),
        'column': article.column.name,
        'image': article.image.image.url
    }


def build_article_page(articles, page_index, page_size):
    """

    :param articles:
    :param page_index:
    :param page_size:
    :return:
    """
    counts = articles.count()
    articles = articles.order_by('-publish_time')[(page_index - 1) * page_size, page_index * page_size]
    return {
        'articles': list(map(read_article, articles)),
        'page_num': (counts // page_size) + (1 if counts % page_size else 0)
    }


def get_article_page_by_column(username, column_id, page_index, page_size=9):
    """

    :param username:
    :param column_id:
    :param page_index:
    :param page_size:
    :return:
    """
    user = get_object_or_404(User, username=username)
    if column_id:
        column = get_object_or_404(Column, pk=column_id)
        articles = column.article_set.filter(author=user, status=ArticleStatus.Published.value)
    else:
        articles = user.article_set.filter(status=ArticleStatus.Published.value)
    return build_article_page(articles, page_index, page_size)


def get_article(username, article_id):
    """

    :param username:
    :param article_id:
    :return:
    """
    user = get_object_or_404(User, username=username)
    article = user.article_set.filter(pk=article_id)
    return read_article(article)


def get_articles(username, page_index, page_size=9):
    user = get_object_or_404(User, username=username)
    articles = user.article_set
    return build_article_page(articles, page_index, page_size)


def create_article(username, image_md5_key, title, content):
    """

    :param username:
    :param image_md5_key:
    :param title:
    :param content:
    :return:
    """
    author = get_object_or_404(User, username=username)
    image = get_object_or_404(Image, md5_key=image_md5_key)
    article = Article(
        title=title,
        author=author,
        content=content,
        image=image,
        create_time=timezone.now(),
    )
    article.save()
    return article.pk
