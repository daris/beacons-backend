# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('beacons', '0004_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='beacon',
            name='store',
            field=models.ForeignKey(related_name='beacons', on_delete=django.db.models.deletion.SET_NULL, db_column=b'store_id', blank=True, to='beacons.Store', null=True),
        ),
    ]
