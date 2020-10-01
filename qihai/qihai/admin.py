from django.contrib import admin


class QihaiAdminSite(admin.AdminSite):
    site_title = 'Qihai Admin'
    site_header = 'Qihai Admin'

    def get_app_list(self, request):
        """
        Return a sorted list of all the installed apps that have been
        registered in this site.
        """
        ordering = {
            'Project': 1,
            'Task': 2,
            'Schedule': 3,
            'Action': 4,
            'User': 6,
            'Group': 7,
        }
        app_dict = self._build_app_dict(request)

        # Sort the apps alphabetically.
        app_list = sorted(app_dict.values(), key=lambda x: x['name'].lower())
        # Sort the models alphabetically within each app.
        for app in app_list:
            app['models'].sort(key=lambda x: ordering[x['object_name']])
        return app_list


admin_qihai = QihaiAdminSite(name='Qihai')

# 必须放在 TodoAdminSite 类的定义之后，否则在 register 时找不到定义
from todo.admin import ProjectAdmin, TaskAdmin, ScheduleAdmin, ActionAdmin
from todo.models import Project, Task, Schedule, Action

admin_qihai.register(Project, ProjectAdmin)
admin_qihai.register(Task, TaskAdmin)
admin_qihai.register(Schedule, ScheduleAdmin)
admin_qihai.register(Action, ActionAdmin)

from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin, GroupAdmin

admin_qihai.register(User, UserAdmin)
admin_qihai.register(Group, GroupAdmin)
