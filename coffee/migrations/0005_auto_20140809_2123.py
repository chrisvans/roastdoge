# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('coffee', '0004_auto_20140802_2001'),
    ]

    operations = [
        migrations.AlterField(
            model_name='greencoffee',
            name='harvest_date',
            field=models.DateTimeField(default=datetime.datetime(2014, 8, 9, 21, 23, 6, 891741)),
        ),
    ]
