# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from decimal import Decimal


class Migration(migrations.Migration):

    dependencies = [
        ('alumni', '0002_auto_20150814_1109'),
    ]

    operations = [
        migrations.AddField(
            model_name='advert',
            name='annual_salary',
            field=models.DecimalField(default=Decimal('0.00'), help_text=b'Annual Salary paid, measured as total cost to company.', max_digits=15, decimal_places=3),
        ),
        migrations.AlterField(
            model_name='advert',
            name='description',
            field=models.CharField(help_text=b'A full description of the job to be advertised.', max_length=255, null=True, blank=True),
        ),
    ]
