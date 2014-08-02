# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import datetime
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('log', '0003_auto_20140801_1732'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='pointcomment',
            options={'ordering': (b'-modified', b'-created'), 'get_latest_by': b'modified'},
        ),
        migrations.AddField(
            model_name='pointcomment',
            name='created',
            field=django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='pointcomment',
            name='modified',
            field=django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='roastprofile',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2014, 8, 2, 20, 1, 42, 823499)),
        ),
    ]
