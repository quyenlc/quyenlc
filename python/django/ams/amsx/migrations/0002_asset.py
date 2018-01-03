# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-29 07:57
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('amsx', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Asset',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('old_code', models.IntegerField()),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('purchased_date', models.DateTimeField(auto_now_add=True)),
                ('availiable_date', models.DateTimeField()),
                ('warranty_start_date', models.DateTimeField()),
                ('warranty_end_date', models.DateTimeField()),
                ('status', models.IntegerField()),
                ('image_url', models.CharField(max_length=256)),
                ('note', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('asset_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='amsx.AssetType')),
                ('group_holder', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.Group')),
                ('holder', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='amsx.Location')),
                ('manufacturer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='amsx.Manufacturer')),
                ('supplier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='amsx.Supplier')),
            ],
        ),
    ]