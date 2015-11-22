# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Beacon',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50, null=True, blank=True)),
                ('uuid', models.CharField(max_length=50, null=True, blank=True)),
                ('minor', models.IntegerField(null=True, blank=True)),
                ('major', models.IntegerField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='SeenOffer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Store',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='StoreOffer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', models.ImageField(null=True, upload_to=b'store_offers', blank=True)),
                ('name', models.CharField(max_length=255, null=True, blank=True)),
                ('store', models.ForeignKey(related_name='offers', db_column=b'store_id', blank=True, to='beacons.Store', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('username', models.CharField(unique=True, max_length=50)),
                ('name', models.CharField(max_length=50)),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='seenoffer',
            name='offer',
            field=models.ForeignKey(related_name='seen_offers', to='beacons.StoreOffer'),
        ),
        migrations.AddField(
            model_name='seenoffer',
            name='user',
            field=models.ForeignKey(related_name='seen_offers', to='beacons.User'),
        ),
        migrations.AddField(
            model_name='beacon',
            name='store',
            field=models.ForeignKey(related_name='beacons', db_column=b'store_id', blank=True, to='beacons.Store', null=True),
        ),
    ]
