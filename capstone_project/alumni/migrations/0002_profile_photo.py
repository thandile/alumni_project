# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import thumbs


class Migration(migrations.Migration):

    dependencies = [
        ('alumni', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='photo',
            field=thumbs.ImageWithThumbsField(null=True, upload_to=b'images'),
        ),
    ]
