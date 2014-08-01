# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('log', '0002_auto_20140801_1632'),
    ]

    operations = [
        migrations.CreateModel(
            name='PointComment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('comment', models.TextField(null=True, blank=True)),
                ('point', models.ForeignKey(blank=True, to='log.TempPoint', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='roastprofile',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2014, 8, 1, 17, 32, 19, 332133)),
        ),
    ]
