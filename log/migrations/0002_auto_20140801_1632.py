# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('log', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='roastprofile',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2014, 8, 1, 16, 32, 39, 228109)),
        ),
    ]
