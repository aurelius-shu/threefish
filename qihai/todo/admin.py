from django.contrib import admin
from todo.models import Project


class ProjectAdmin(admin.ModelAdmin):
    fieldsets = [
        ('base info', {'fields': ['name', 'type', 'status', 'owner', 'create_time', 'comment']})
    ]
    list_display = (
        'name', 'type', 'status', 'owner', 'create_time', 'update_time', 'comment'
    )
    ordering = ['-update_time']
    list_filter = ['type', 'status']
    search_fields = ['name', 'create_time', 'comment']


admin.site.register(Project, ProjectAdmin)

admin.site.site_title = 'qihai'

admin.site.site_header = 'to-do'
