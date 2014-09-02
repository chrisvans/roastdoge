# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('profiling', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='roastprofile',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2014, 9, 2, 22, 49, 13, 812510)),
        ),
    ]
