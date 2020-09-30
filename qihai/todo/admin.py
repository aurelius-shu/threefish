from django.contrib import admin
from todo.models import Project, Task, Schedule, Step


class ProjectAdmin(admin.ModelAdmin):
    fieldsets = [
        ('base info', {'fields': ['name', 'type', 'status', 'owner', 'comment']})
    ]
    list_display = (
        'name', 'type', 'status', 'owner', 'create_time', 'update_time', 'comment'
    )
    ordering = ['-update_time']
    list_filter = ['type', 'status', 'create_time']
    search_fields = ['name', 'create_time', 'comment']


class TaskAdmin(admin.ModelAdmin):
    fieldsets = [
        ('base info', {'fields': ['keyword', 'project', 'status', 'description', ]})
    ]
    list_display = (
        'project', 'keyword', 'status', 'create_time', 'update_time', 'description',
    )
    ordering = ['-update_time']
    list_filter = ['status', 'create_time', 'project']
    search_fields = ['keyword', 'create_time', 'description']


class ScheduleAdmin(admin.ModelAdmin):
    fieldsets = [
        ('base info', {'fields': ['keyword', 'status', 'start_time', 'end_time', 'comment', ]})
    ]
    list_display = (
        'keyword', 'status', 'create_time', 'update_time', 'start_time', 'end_time', 'comment',
    )
    ordering = ['-update_time']
    list_filter = ['status', 'start_time', 'keyword', ]
    search_fields = ['keyword', 'status', 'start_time', 'comment']


class StepAdmin(admin.ModelAdmin):
    fieldsets = [
        ('base info', {'fields': ['schedule', 'task', 'status', 'start_time', 'end_time', 'outcome', ]})
    ]
    list_display = (
        'schedule', 'task', 'status', 'create_time', 'update_time', 'start_time', 'end_time', 'outcome',
    )
    ordering = ['-update_time']
    list_filter = ['status', 'start_time', 'schedule', 'task', ]
    search_fields = ['schedule', 'task', 'status', 'start_time', 'outcome']


# todo:
#  1. task / step 添加 project 过滤
#  2. 添加完成操作，未完成操作


admin.site.register(Project, ProjectAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(Schedule, ScheduleAdmin)
admin.site.register(Step, StepAdmin)

admin.site.site_title = 'qihai'
admin.site.site_header = 'to-do'
