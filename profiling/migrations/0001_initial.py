# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import datetime
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('coffee', '0002_auto_20140902_2249'),
    ]

    operations = [
        migrations.CreateModel(
            name='PointComment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('comment', models.TextField(null=True, blank=True)),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RoastProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('date', models.DateTimeField(default=datetime.datetime(2014, 9, 2, 22, 49, 5, 228766))),
                ('coffee', models.ForeignKey(to='coffee.Coffee', null=True)),
            ],
            options={
                'verbose_name': 'Roast Profile',
                'verbose_name_plural': 'Roast Profiles',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TempPoint',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('temperature', models.CharField(default='212.0', max_length=255)),
                ('time', models.PositiveIntegerField()),
                ('roast_profile', models.ForeignKey(to='profiling.RoastProfile')),
            ],
            options={
                'verbose_name': 'Temperature Point',
                'verbose_name_plural': 'Temperature Points',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='pointcomment',
            name='point',
            field=models.ForeignKey(blank=True, to='profiling.TempPoint', null=True),
            preserve_default=True,
        ),
    ]
