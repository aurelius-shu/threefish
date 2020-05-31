from django.shortcuts import get_object_or_404
from ..models import User
from datetime import datetime


def read_column(column):
    """

    :param column:
    :return:
    """
    return {
        'id': column.pk,
        'name': column.name,
        'comment': column.comment,
        'author': column.author.username,
        'create_time': datetime.strftime(column.create_time, '%Y-%m-%d %H:%M:%S'),
        'update_time': datetime.strftime(column.update_time, '%Y-%m-%d %H:%M:%S'),
        'is_delete': column.is_delete
    }


def get_columns(username):
    """

    :param username:
    :return:
    """
    user = get_object_or_404(User, username=username)
    columns = user.column_set.filter(is_delete=False).order_by('-update_time')
    return list(map(read_column, columns))
