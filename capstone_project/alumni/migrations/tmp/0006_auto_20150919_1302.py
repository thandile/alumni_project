# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from decimal import Decimal


class Migration(migrations.Migration):

    dependencies = [
        ('alumni', '0005_auto_20150918_1239'),
    ]

    operations = [
        migrations.AddField(
            model_name='advert',
            name='contact_details',
            field=models.EmailField(default='jarryd.garisch@gmail.com', max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='advert',
            name='annual_salary',
            field=models.DecimalField(default=Decimal('0.00'), help_text=b'Gross annual. Please provide further salary details under description.', max_digits=15, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='advert',
            name='closing_date',
            field=models.DateTimeField(null=True),
        ),
    ]
