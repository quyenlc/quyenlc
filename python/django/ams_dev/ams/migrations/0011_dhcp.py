# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-10 03:15
from __future__ import unicode_literals

from django.db import migrations, models
import django_unixdatetimefield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('ams', '0010_auto_20171010_0941'),
    ]

    operations = [
        migrations.CreateModel(
            name='DHCP',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mac_addr', models.CharField(max_length=32)),
                ('device_id', models.IntegerField(default=0)),
                ('ip_addr', models.CharField(max_length=64)),
                ('hostname', models.CharField(max_length=64)),
                ('created_at', django_unixdatetimefield.fields.UnixDateTimeField(editable=False)),
                ('updated_at', django_unixdatetimefield.fields.UnixDateTimeField(editable=False)),
            ],
        ),
    ]
