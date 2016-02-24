# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('beacons', '0002_store_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='store',
            name='description',
            field=models.TextField(null=True, blank=True),
        ),
    ]
