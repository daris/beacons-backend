# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('beacons', '0003_auto_20160224_1903'),
    ]

    operations = [
        migrations.CreateModel(
            name='Token',
            fields=[
                ('token', models.CharField(max_length=40, serialize=False, primary_key=True)),
                ('expire_at', models.DateTimeField()),
                ('last_active_at', models.DateTimeField(auto_now_add=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('device_id', models.CharField(max_length=255, null=True, blank=True)),
                ('user', models.ForeignKey(related_name='tokens', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
