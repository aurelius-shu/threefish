from django.contrib import admin
from todo.models import Project, Task, Schedule, Step


class TaskInline(admin.TabularInline):
    model = Task
    extra = 0


class StepInline(admin.TabularInline):
    model = Step
    extra = 0


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    fieldsets = (
        ('基础信息', {
            'fields': (('name', 'type', 'owner'), ('comment', 'status'))
        }),
    )
    list_display = (
        'name', 'type', 'status', 'owner', 'create_time', 'update_time', 'comment', 'was_completed'
    )
    inlines = [TaskInline]
    ordering = ['-update_time']
    list_filter = ['type', 'status', 'create_time']
    search_fields = ['name', 'create_time', 'comment']
    list_per_page = 15


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    fieldsets = [
        ('基础信息', {'fields': [('keyword', 'project'), ('description', 'status'), ]})
    ]
    list_display = (
        'project', 'keyword', 'status', 'create_time', 'update_time', 'description', 'was_completed'
    )
    ordering = ['-update_time']
    list_filter = ['status', 'create_time', 'project']
    search_fields = ['keyword', 'create_time', 'description']
    list_per_page = 15


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    fieldsets = [
        ('基础信息', {'fields': [('keyword', 'status'), ('start_time', 'end_time'), 'comment', ]})
    ]
    list_display = (
        'keyword', 'status', 'create_time', 'update_time', 'start_time', 'end_time', 'comment', 'was_completed'
    )
    inlines = [StepInline]
    ordering = ['-update_time']
    list_filter = ['status', 'start_time', 'keyword', ]
    search_fields = ['keyword', 'status', 'start_time', 'comment']
    list_per_page = 15


@admin.register(Step)
class StepAdmin(admin.ModelAdmin):
    fieldsets = [
        ('基础信息', {'fields': [('schedule', 'task'), ('start_time', 'end_time'), ('outcome', 'status'), ]})
    ]
    list_display = (
        'schedule', 'task', 'project', 'status', 'create_time', 'update_time', 'start_time', 'end_time', 'outcome',
        'was_completed'
    )
    ordering = ['-update_time']
    list_filter = ['status', 'start_time', 'task__project', 'schedule', 'task']
    search_fields = ['schedule', 'task', 'status', 'start_time', 'outcome']
    list_per_page = 15


# todo:
#  1. 添加完成操作，未完成操作


admin.site.site_title = 'qihai'
admin.site.site_header = 'to-do'
