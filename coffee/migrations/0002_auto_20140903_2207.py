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
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
