# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Advert',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('city', models.CharField(max_length=255, blank=True, null=True)),
                ('country', models.CharField(max_length=255, blank=True, null=True)),
                ('title', models.CharField(max_length=255, blank=True, null=True)),
                ('description', models.CharField(max_length=255, blank=True, null=True)),
                ('reference', models.CharField(max_length=255, blank=True, null=True)),
                ('closing_date', models.DateTimeField()),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('last_updated_date', models.DateTimeField(auto_now=True)),
                ('creating_user', models.ForeignKey(related_name='advert_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('street', models.CharField(max_length=255, blank=True, null=True)),
                ('city', models.CharField(max_length=255, blank=True, null=True)),
                ('country', models.CharField(max_length=255, blank=True, null=True)),
                ('title', models.CharField(max_length=255, blank=True, null=True)),
                ('description', models.CharField(max_length=255, blank=True, null=True)),
                ('event_type', models.CharField(max_length=255, blank=True, null=True)),
                ('year', models.IntegerField(blank=True, null=True)),
                ('month', models.IntegerField(blank=True, null=True)),
                ('day', models.IntegerField(blank=True, null=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('last_updated_date', models.DateTimeField(auto_now=True)),
                ('creating_user', models.ForeignKey(related_name='event_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Forum',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('title', models.CharField(max_length=255, blank=True, null=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('last_updated_date', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('job_profile', models.IntegerField()),
                ('company_name', models.CharField(max_length=255, blank=True, null=True)),
                ('job_title', models.CharField(max_length=255, blank=True, null=True)),
                ('job_desc', models.CharField(max_length=255, blank=True, null=True)),
                ('job_location', models.CharField(max_length=255, blank=True, null=True)),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('last_updated_date', models.DateTimeField(auto_now=True)),
                ('job_number', models.CharField(max_length=10, blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('title', models.CharField(max_length=255, blank=True, null=True)),
                ('text', models.TextField(max_length=10000)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('last_updated_date', models.DateTimeField(auto_now=True)),
                ('creating_user', models.ForeignKey(related_name='post_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('city', models.CharField(max_length=255, blank=True, null=True)),
                ('country', models.CharField(max_length=255, blank=True, null=True)),
                ('grad_year', models.IntegerField(blank=True, null=True)),
                ('degree', models.CharField(max_length=255, blank=True, null=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('last_updated_date', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(related_name='user_obj', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Thread',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('title', models.CharField(max_length=255, blank=True, null=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('last_updated_date', models.DateTimeField(auto_now=True)),
                ('creating_user', models.ForeignKey(related_name='thread_user', to=settings.AUTH_USER_MODEL)),
                ('forum', models.ForeignKey(to='alumni.Forum')),
            ],
        ),
        migrations.AddField(
            model_name='post',
            name='thread',
            field=models.ForeignKey(to='alumni.Thread'),
        ),
    ]
