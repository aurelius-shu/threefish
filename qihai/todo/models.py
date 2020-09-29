from enum import Enum, unique
from django.db.models import Model, IntegerField, CharField


@unique
class Project_Status(Enum):
    doing = 1
    done = 2
    closed = 3


class Project(Model):
    id = IntegerField(primary_key=True)
    name = CharField(max_length=30, default=' ')
    type = CharField(max_length=30, default=' ')
    # status =
