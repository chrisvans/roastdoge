# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('coffee', '0002_auto_20140801_1632'),
    ]

    operations = [
        migrations.AlterField(
            model_name='greencoffee',
            name='harvest_date',
            field=models.DateTimeField(default=datetime.datetime(2014, 8, 1, 17, 32, 19, 323717)),
        ),
    ]
