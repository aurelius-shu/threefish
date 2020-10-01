from django.contrib.admin.apps import AdminConfig


class QihaiAdminConfig(AdminConfig):
    default_site = 'qihai.admin.QihaiAdminSite'
