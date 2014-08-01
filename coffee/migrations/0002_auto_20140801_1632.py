# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('coffee', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='greencoffeecomponent',
            name='coffee',
        ),
        migrations.RemoveField(
            model_name='greencoffeecomponent',
            name='green_coffee',
        ),
        migrations.DeleteModel(
            name='GreenCoffeeComponent',
        ),
        migrations.AddField(
            model_name='greencoffee',
            name='region',
            field=models.CharField(max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='greencoffee',
            name='description',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='greencoffee',
            name='farm',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='greencoffee',
            name='harvest_date',
            field=models.DateTimeField(default=datetime.datetime(2014, 8, 1, 16, 32, 39, 221552)),
        ),
    ]
