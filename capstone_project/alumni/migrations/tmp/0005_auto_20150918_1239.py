# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from decimal import Decimal


class Migration(migrations.Migration):

    dependencies = [
        ('alumni', '0004_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advert',
            name='annual_salary',
            field=models.DecimalField(default=Decimal('0.00'), help_text=b'Please note that annual salary is measured as total cost to company (in ZAR).', max_digits=15, decimal_places=2),
        ),
    ]
