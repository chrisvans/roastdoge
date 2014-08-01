# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('coffee', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RoastProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255)),
                ('date', models.DateTimeField(default=datetime.datetime(2014, 8, 1, 1, 51, 36, 239083))),
                ('coffee', models.ForeignKey(to='coffee.Coffee', null=True)),
            ],
            options={
                'verbose_name': b'Roast Profile',
                'verbose_name_plural': b'Roast Profiles',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TempPoint',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('temperature', models.CharField(default='212.0', max_length=255)),
                ('time', models.PositiveIntegerField()),
                ('roast_profile', models.ForeignKey(to='log.RoastProfile')),
            ],
            options={
                'verbose_name': b'Temperature Point',
                'verbose_name_plural': b'Temperature Points',
            },
            bases=(models.Model,),
        ),
    ]
