from qihai.realm.models import User


def read_user(user):
    """

    :param user:
    :return:
    """

    return {
        'id': user.pk,
        'username': user.username,
        'phone': user.phone,
        'email': user.email,
        'reg_time': user.reg_time,
        'last_login': user.last_login,
        'is_active': user.is_active,
    }


def get_users_page(page_index, page_size=9):
    """

    :param page_index:
    :param page_size:
    :return:
    """

    users = User.objects.all().order_by('-reg_time')[(page_index - 1) * page_size:page_index * page_size]
    counts = User.objects.count()
    return {
        'users': list(map(read_user, users)),
        'page_nums': counts // page_size + (1 if counts % page_size else 0)
    }
