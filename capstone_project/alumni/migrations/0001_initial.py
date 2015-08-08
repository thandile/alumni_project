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
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('city', models.CharField(max_length=255, null=True, blank=True)),
                ('country', models.CharField(max_length=255, null=True, blank=True)),
                ('title', models.CharField(max_length=255, null=True, blank=True)),
                ('description', models.CharField(max_length=255, null=True, blank=True)),
                ('reference', models.CharField(max_length=255, null=True, blank=True)),
                ('closing_date', models.DateTimeField()),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('last_updated_date', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(related_name='advert_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('street', models.CharField(max_length=255, null=True, blank=True)),
                ('city', models.CharField(max_length=255, null=True, blank=True)),
                ('country', models.CharField(max_length=255, null=True, blank=True)),
                ('title', models.CharField(max_length=255, null=True, blank=True)),
                ('description', models.CharField(max_length=255, null=True, blank=True)),
                ('event_type', models.CharField(max_length=255, null=True, blank=True)),
                ('event_date', models.DateTimeField()),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('last_updated_date', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(related_name='event_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('company_name', models.CharField(max_length=255, null=True, blank=True)),
                ('job_desc', models.CharField(max_length=255, null=True, blank=True)),
                ('job_title', models.CharField(max_length=255, null=True, blank=True)),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('last_updated_date', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('city', models.CharField(max_length=255, null=True, blank=True)),
                ('country', models.CharField(max_length=255, null=True, blank=True)),
                ('degree', models.CharField(max_length=255, null=True, blank=True)),
                ('grad_year', models.IntegerField(null=True, blank=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('last_updated_date', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(related_name='user_obj', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
