# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('coffee', '0003_auto_20140801_1732'),
    ]

    operations = [
        migrations.AlterField(
            model_name='greencoffee',
            name='harvest_date',
            field=models.DateTimeField(default=datetime.datetime(2014, 8, 2, 20, 1, 42, 799436)),
        ),
    ]
