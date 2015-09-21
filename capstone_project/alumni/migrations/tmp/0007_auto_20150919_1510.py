# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('alumni', '0006_auto_20150919_1302'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advert',
            name='closing_date',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]
