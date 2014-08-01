# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

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
                ('farm', models.CharField(max_length=255, null=True)),
                ('varietal', models.CharField(max_length=255, null=True, blank=True)),
                ('harvest_date', models.DateTimeField(default=datetime.datetime(2014, 8, 1, 1, 51, 36, 231272))),
                ('description', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='GreenCoffeeComponent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('percent', models.PositiveIntegerField()),
                ('coffee', models.ForeignKey(blank=True, to='coffee.Coffee', null=True)),
                ('green_coffee', models.ForeignKey(to='coffee.GreenCoffee')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
