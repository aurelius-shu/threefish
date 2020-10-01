from enum import Enum, unique
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


@unique
class ProjectType(Enum):
    学习 = 1
    工作 = 2
    生活 = 3
    其他 = 4


@unique
class Status(Enum):
    正在进行 = 1
    完成 = 2
    关闭 = 3


def consuming_format(delta):
    if delta < 60:
        return f'{delta}秒'
    if delta < 3600:
        return f'{(delta // 60)}分钟'
    if delta < 86400:
        return f'{(delta // 3600)}小时 {(delta % 3600) // 60}分钟'
    else:
        return f'{(delta // 86400)}天 {(delta % 86400) // 3600}小时'


class Project(models.Model):
    name = models.CharField('名称', max_length=30, default=' ')
    type = models.IntegerField('类型', default=4, choices=[(tag.value, tag.name) for tag in ProjectType])
    status = models.IntegerField('状态', default=1, choices=[(tag.value, tag.name) for tag in Status])
    owner = models.ForeignKey(User, verbose_name='归属', null=True, on_delete=models.SET_NULL, related_name='projects')
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    update_time = models.DateTimeField('更新时间', auto_now=True)
    comment = models.CharField('备注', max_length=255, default=' ')

    def was_completed(self):
        return Status.完成.value == self.status

    was_completed.admin_order_field = 'update_time'
    was_completed.boolean = True
    was_completed.short_description = '是否完成'

    def __str__(self):
        return f"{ProjectType(self.type).name} | {self.name}"

    class Meta:
        verbose_name = '项目'
        verbose_name_plural = '项目'


class Task(models.Model):
    project = models.ForeignKey(Project, verbose_name='所属项目', on_delete=models.CASCADE, related_name='tasks')
    keyword = models.CharField('关键字', max_length=30, default=' ')
    status = models.IntegerField('状态', default=1, choices=[(tag.value, tag.name) for tag in Status])
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    update_time = models.DateTimeField('更新时间', auto_now=True)
    description = models.CharField('描述', max_length=255, default=' ')

    def was_completed(self):
        return Status.完成.value == self.status

    was_completed.admin_order_field = 'update_time'
    was_completed.boolean = True
    was_completed.short_description = '是否完成'

    def __str__(self):
        return f"{ProjectType(self.project.type).name} | {self.project.name} | {self.keyword}"

    class Meta:
        verbose_name = '任务'
        verbose_name_plural = '任务'


class Schedule(models.Model):
    keyword = models.CharField('关键字', max_length=30, default=' ')
    status = models.IntegerField('状态', default=1, choices=[(tag.value, tag.name) for tag in Status])
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    update_time = models.DateTimeField('更新时间', auto_now=True)
    start_time = models.DateTimeField('计划开始', default=timezone.now)
    end_time = models.DateTimeField('计划结束', default=timezone.now)
    comment = models.CharField('备注', max_length=255, default=' ')

    def was_completed(self):
        return Status.完成.value == self.status

    def consume(self):
        delta = (self.end_time - self.start_time).seconds
        return consuming_format(delta)

    was_completed.admin_order_field = 'update_time'
    was_completed.boolean = True
    was_completed.short_description = '是否完成'
    consume.short_description = '计划耗时'

    def __str__(self):
        return f"{self.start_time.astimezone(timezone.get_current_timezone()).strftime('%m-%d')} -> {self.end_time.astimezone(timezone.get_current_timezone()).strftime('%m-%d')} | {self.keyword}"

    class Meta:
        verbose_name = '计划'
        verbose_name_plural = '计划'


class Action(models.Model):
    schedule = models.ForeignKey(Schedule, verbose_name='预约表', on_delete=models.CASCADE, related_name='actions')
    task = models.ForeignKey(Task, verbose_name='针对任务', on_delete=models.CASCADE, related_name='actions')
    status = models.IntegerField('状态', default=1, choices=[(tag.value, tag.name) for tag in Status])
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    update_time = models.DateTimeField('更新时间', auto_now=True)
    start_time = models.DateTimeField('开始时间', default=timezone.now)
    end_time = models.DateTimeField('结束时间', default=timezone.now)
    outcome = models.CharField('产出', max_length=255, default='未完成')

    def was_completed(self):
        return Status.完成.value == self.status

    def consume(self):
        delta = (self.end_time - self.start_time).seconds
        return consuming_format(delta)

    was_completed.admin_order_field = 'update_time'
    was_completed.boolean = True
    was_completed.short_description = '是否完成'
    consume.short_description = '耗时'

    def __str__(self):
        return f"{self.start_time.astimezone(timezone.get_current_timezone()).strftime('%m-%d')}({self.start_time.astimezone(timezone.get_current_timezone()).strftime('%H:%M')} -> {self.end_time.astimezone(timezone.get_current_timezone()).strftime('%H:%M')})"

    class Meta:
        verbose_name = '事件'
        verbose_name_plural = '事件'
