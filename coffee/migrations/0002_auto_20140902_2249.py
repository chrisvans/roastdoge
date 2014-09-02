# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('coffee', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='greencoffee',
            name='harvest_date',
            field=models.DateTimeField(default=datetime.datetime(2014, 9, 2, 22, 49, 5, 194496)),
        ),
    ]
