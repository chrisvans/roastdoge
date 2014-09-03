# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    replaces = [(b'coffee', '0001_initial'), (b'coffee', '0002_auto_20140903_2207'), (b'coffee', '0003_auto_20140903_2237')]

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Coffee',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='GreenCoffee',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255)),
                ('country', models.CharField(max_length=255, null=True)),
                ('region', models.CharField(max_length=255, null=True, blank=True)),
                ('farm', models.CharField(max_length=255, null=True, blank=True)),
                ('varietal', models.CharField(max_length=255, null=True, blank=True)),
                ('harvest_date', models.DateTimeField(default=datetime.datetime.now)),
                ('description', models.TextField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
