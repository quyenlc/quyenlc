# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-09 14:59
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ams', '0008_adcomputer'),
    ]

    operations = [
        migrations.RenameField(
            model_name='adcomputer',
            old_name='username',
            new_name='email',
        ),
    ]
