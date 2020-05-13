# Generated by Django 3.0.6 on 2020-05-13 15:44

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=200)),
                ('nickname', models.CharField(max_length=200)),
                ('phone', models.CharField(max_length=13)),
                ('email', models.CharField(max_length=30)),
                ('password', models.CharField(max_length=128)),
                ('reg_time', models.DateTimeField(verbose_name='time registered')),
                ('last_login', models.DateTimeField(verbose_name='time last login')),
                ('status', models.BooleanField(verbose_name='active or inactive')),
            ],
        ),
    ]