# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('profiling', '0002_auto_20140902_2249'),
    ]

    operations = [
        migrations.AddField(
            model_name='roastprofile',
            name='_graph_data_cache',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='roastprofile',
            name='date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
