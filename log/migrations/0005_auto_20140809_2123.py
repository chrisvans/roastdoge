# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('log', '0004_auto_20140802_2001'),
    ]

    operations = [
        migrations.AlterField(
            model_name='roastprofile',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2014, 8, 9, 21, 23, 6, 917535)),
        ),
        migrations.AlterField(
            model_name='roastprofile',
            name='name',
            field=models.CharField(max_length=255),
        ),
    ]
