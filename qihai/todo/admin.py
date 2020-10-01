from django.contrib import admin

from todo.models import Task, Action, Status, Project, Schedule


class TaskInline(admin.TabularInline):
    model = Task
    extra = 0


class ActionInline(admin.TabularInline):
    model = Action
    extra = 0


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    def make_completed(self, request, queryset):
        queryset.update(status=Status.完成.value)

    make_completed.short_description = "完成所选的 项目"

    actions = ['make_completed']

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
    search_fields = ['name', 'update_time', 'comment']
    list_per_page = 25


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    def make_completed(self, request, queryset):
        queryset.update(status=Status.完成.value)

    make_completed.short_description = "完成所选的 任务"

    actions = ['make_completed']

    fieldsets = [
        ('基础信息', {'fields': [('keyword', 'project'), ('description', 'status'), ]})
    ]
    list_display = (
        'project', 'keyword', 'status', 'create_time', 'update_time', 'description', 'was_completed'
    )
    ordering = ['-update_time']
    list_filter = ['status', 'update_time', 'project__type', 'project']
    search_fields = ['keyword', 'create_time', 'description']
    list_per_page = 25


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    def make_completed(self, request, queryset):
        queryset.update(status=Status.完成.value)

    make_completed.short_description = "完成所选的 计划"

    actions = ['make_completed']

    fieldsets = [
        ('基础信息', {'fields': [('keyword', 'status'), ('start_time', 'end_time'), 'comment', ]})
    ]
    list_display = (
        'keyword', 'status', 'start_time', 'end_time', 'consume', 'create_time', 'update_time', 'comment',
        'was_completed'
    )
    inlines = [ActionInline]
    ordering = ['-start_time']
    list_filter = ['status', 'update_time', 'keyword', ]
    search_fields = ['keyword', 'status', 'start_time', 'comment']
    list_per_page = 25


@admin.register(Action)
class ActionAdmin(admin.ModelAdmin):
    def make_completed(self, request, queryset):
        queryset.update(status=Status.完成.value)

    def make_undone(self, request, queryset):
        queryset.update(status=Status.正在进行.value)

    make_completed.short_description = "完成所选的 事件"
    make_undone.short_description = "重启所选的 事件"

    actions = ['make_completed', 'make_undone']

    fieldsets = [
        ('基础信息', {'fields': [('schedule', 'task'), ('start_time', 'end_time'), ('outcome', 'status'), ]})
    ]
    list_display = (
        'schedule', 'task', 'status', 'start_time', 'end_time', 'consume', 'outcome', 'create_time', 'update_time',
        'was_completed'
    )
    ordering = ['-start_time']
    list_filter = ['schedule', 'task__project__type', 'status', 'start_time', 'task__project']
    search_fields = ['schedule', 'task', 'status', 'start_time', 'outcome']
    list_per_page = 25
