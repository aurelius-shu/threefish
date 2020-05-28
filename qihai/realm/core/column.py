from django.shortcuts import get_object_or_404
from qihai.realm.models import User, Column
from datetime import datetime


def read_column(column):
    """

    :param column:
    :return:
    """
    return {
        'name': column.name,
        'comment': column.comment,
        'author': column.author.username,
        'create_time': datetime.strftime(column.create_time, '%Y-%m-%d %H:%M:%S'),
        'update_time': datetime.strftime(column.update_time, '%Y-%m-%d %H:%M:%S'),
        'is_delete': column.is_delete
    }


def get_columns(username):
    user = get_object_or_404(User, username=username)
    columns = user.column_set.filter(is_delete=False).order_by('-update_time')
    return list(map(read_column, columns))
