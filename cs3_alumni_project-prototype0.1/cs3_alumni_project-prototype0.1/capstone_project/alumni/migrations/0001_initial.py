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
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('city', models.CharField(null=True, blank=True, max_length=255)),
                ('country', models.CharField(null=True, blank=True, max_length=255)),
                ('title', models.CharField(null=True, blank=True, max_length=255)),
                ('description', models.CharField(null=True, blank=True, max_length=255)),
                ('reference', models.CharField(null=True, blank=True, max_length=255)),
                ('closing_date', models.DateTimeField()),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('last_updated_date', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='advert_user')),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('street', models.CharField(null=True, blank=True, max_length=255)),
                ('city', models.CharField(null=True, blank=True, max_length=255)),
                ('country', models.CharField(null=True, blank=True, max_length=255)),
                ('title', models.CharField(null=True, blank=True, max_length=255)),
                ('description', models.CharField(null=True, blank=True, max_length=255)),
                ('event_type', models.CharField(null=True, blank=True, max_length=255)),
                ('event_date', models.DateTimeField()),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('last_updated_date', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='event_user')),
            ],
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('company_name', models.CharField(null=True, blank=True, max_length=255)),
                ('job_desc', models.CharField(null=True, blank=True, max_length=255)),
                ('job_title', models.CharField(null=True, blank=True, max_length=255)),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('last_updated_date', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('city', models.CharField(null=True, blank=True, max_length=255)),
                ('country', models.CharField(null=True, blank=True, max_length=255)),
                ('grad_year', models.IntegerField(null=True, blank=True)),
                ('degree', models.CharField(null=True, blank=True, max_length=255)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('last_updated_date', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='user_obj')),
            ],
        ),
    ]
