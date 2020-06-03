from django.shortcuts import get_object_or_404
from ..models import User, Column, ArticleStatus, Image, Article
from datetime import datetime
from django.utils import timezone


def read_article_brief(article):
    """

    :param article:
    :return:
    """
    return {
        'id': article.pk,
        'title': article.title,
        'column_id': article.column.id,
        'column': article.column.name,
        'author': article.author.username,
        'card': article.card.image.url,
        'comment': article.comment,
        'status': ArticleStatus(article.status).name,
        'create_time': datetime.strftime(article.create_time, '%Y-%m-%d %H:%M:%S') if article.create_time else None,
        'update_time': datetime.strftime(article.update_time, '%Y-%m-%d %H:%M:%S') if article.update_time else None,
        'publish_time': datetime.strftime(article.publish_time, '%Y-%m-%d %H:%M:%S') if article.publish_time else None,
    }


def read_article(article):
    """

    :param article:
    :return:
    """
    return {
        'id': article.pk,
        'title': article.title,
        'column_id': article.column.id,
        'column': article.column.name,
        'author': article.author.username,
        'card': article.card.image.url,
        'comment': article.comment,
        'status': ArticleStatus(article.status).name,
        'create_time': datetime.strftime(article.create_time, '%Y-%m-%d %H:%M:%S') if article.create_time else None,
        'update_time': datetime.strftime(article.update_time, '%Y-%m-%d %H:%M:%S') if article.update_time else None,
        'publish_time': datetime.strftime(article.publish_time, '%Y-%m-%d %H:%M:%S') if article.publish_time else None,
        'content': article.content,
    }


def build_article_page(articles, page_index, page_size):
    """

    :param articles:
    :param page_index:
    :param page_size:
    :return:
    """
    counts = articles.count()
    articles = articles.order_by('-publish_time')[(page_index - 1) * page_size: page_index * page_size]
    return {
        'articles': list(map(read_article_brief, articles)),
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
    article = user.article_set.get(pk=article_id)
    return read_article(article)


def get_articles(username, page_index, page_size=9):
    """

    :param username:
    :param page_index:
    :param page_size:
    :return:
    """
    user = get_object_or_404(User, username=username)
    articles = user.article_set
    return build_article_page(articles, page_index, page_size)


def create_article(username, title, column_id, image_md5_key, comment, content):
    """

    :param username:
    :param title:
    :param column_id:
    :param image_md5_key:
    :param comment:
    :param content:
    :return:
    """
    author = get_object_or_404(User, username=username)
    image = get_object_or_404(Image, md5_key=image_md5_key)
    column = get_object_or_404(Column, pk=column_id)
    article = Article(
        title=title,
        column=column,
        author=author,
        image=image,
        comment=comment,
        content=content,
    )
    article.save()
    return article.pk


def edit_article(username, article_id):
    """

    :param username:
    :param article_id:
    :return:
    """
    author = get_object_or_404(User, username=username)
    article = get_object_or_404(Article, pk=article_id, author=author)
    return read_article(article)


def update_article(username, article_id, **kwargs):
    """

    :param username:
    :param article_id:
    :param kwargs:
    :return:
    """
    author = get_object_or_404(User, username=username)
    article = get_object_or_404(Article, pk=article_id, author=author)

    # title, column_id, image_md5_key, comment, content
    if 'title' in kwargs:
        article.update(title=kwargs['title'])
    if 'column_id' in kwargs:
        column = get_object_or_404(Column, pk=kwargs['column_id'])
        article.update(column=column)
    if 'image_md5_key' in kwargs:
        image = get_object_or_404(Image, md5_key=kwargs['image_md5_key'])
        article.update(image=image)
    if 'comment' in kwargs:
        article.update(comment=kwargs['comment'])
    if 'content' in kwargs:
        article.update(content=kwargs['content'])

    article.update(update_time=timezone.now())
    return True


def remove_article(username, article_id):
    """

    :param username:
    :param article_id:
    :return:
    """
    author = get_object_or_404(User, username=username)
    article = get_object_or_404(Article, pk=article_id, author=author)
    article.update(status=ArticleStatus.Removed.value)
    article.update(update_time=timezone.now())
    return True


def publish_article(username, article_id):
    """

    :param username:
    :param article_id:
    :return:
    """
    author = get_object_or_404(User, username=username)
    article = Article.objects.filter(pk=article_id, author=author)
    article.update(status=ArticleStatus.Published.value)
    article.update(publish_time=timezone.now())
    article.update(update_time=timezone.now())
    return True
