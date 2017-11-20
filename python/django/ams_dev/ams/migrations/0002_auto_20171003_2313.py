# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-03 16:13
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django_unixdatetimefield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('ams', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='computer',
            old_name='device_id',
            new_name='device',
        ),
        migrations.RenameField(
            model_name='computersoftwares',
            old_name='device_id',
            new_name='device',
        ),
        migrations.RenameField(
            model_name='computersoftwares',
            old_name='software_id',
            new_name='software',
        ),
        migrations.RenameField(
            model_name='device',
            old_name='location_id',
            new_name='location',
        ),
        migrations.RenameField(
            model_name='device',
            old_name='manufacture_id',
            new_name='manufacture',
        ),
        migrations.RenameField(
            model_name='device',
            old_name='supplier_id',
            new_name='supplier',
        ),
        migrations.RenameField(
            model_name='devicechangelog',
            old_name='device_id',
            new_name='device',
        ),
        migrations.RenameField(
            model_name='devicechangelog',
            old_name='user_id',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='history',
            old_name='from_user_id',
            new_name='from_user',
        ),
        migrations.RenameField(
            model_name='history',
            old_name='item_id',
            new_name='item',
        ),
        migrations.RenameField(
            model_name='history',
            old_name='to_user_id',
            new_name='to_user',
        ),
        migrations.RenameField(
            model_name='inuses',
            old_name='computer_id',
            new_name='computer',
        ),
        migrations.RenameField(
            model_name='inuses',
            old_name='license_id',
            new_name='license',
        ),
        migrations.RenameField(
            model_name='license',
            old_name='software_group_id',
            new_name='software_group',
        ),
        migrations.RenameField(
            model_name='licensesoftware',
            old_name='license_id',
            new_name='license',
        ),
        migrations.RenameField(
            model_name='licensesoftware',
            old_name='software_id',
            new_name='software',
        ),
        migrations.RenameField(
            model_name='macaddress',
            old_name='device_id',
            new_name='device',
        ),
        migrations.RenameField(
            model_name='software',
            old_name='software_group_id',
            new_name='software_group',
        ),
        migrations.RenameField(
            model_name='usersoftware',
            old_name='license_id',
            new_name='license',
        ),
        migrations.RenameField(
            model_name='usersoftware',
            old_name='license_software_id',
            new_name='license_software',
        ),
        migrations.RenameField(
            model_name='usersoftware',
            old_name='user_id',
            new_name='user',
        ),
        migrations.RemoveField(
            model_name='computer',
            name='orange_status',
        ),
        migrations.RemoveField(
            model_name='computer',
            name='orange_version',
        ),
        migrations.RemoveField(
            model_name='device',
            name='type',
        ),
        migrations.AddField(
            model_name='device',
            name='device_type',
            field=models.CharField(blank=True, db_column='type', max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='computer',
            name='ad_binding',
            field=models.BooleanField(),
        ),
        migrations.AlterField(
            model_name='computer',
            name='antivirus_software',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Antivirus(AV) Software'),
        ),
        migrations.AlterField(
            model_name='computer',
            name='antivirus_ver',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Version of AV software'),
        ),
        migrations.AlterField(
            model_name='computer',
            name='auto',
            field=models.IntegerField(choices=[(None, '-- Please choose a value --'), (0, 'Automatic'), (1, 'Manually')]),
        ),
        migrations.AlterField(
            model_name='computer',
            name='created_at',
            field=django_unixdatetimefield.fields.UnixDateTimeField(blank=True, editable=False, null=True),
        ),
        migrations.AlterField(
            model_name='computer',
            name='fde_software',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Full Disk Encryption(FDE) Software'),
        ),
        migrations.AlterField(
            model_name='computer',
            name='fde_ver',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Version of FDE software'),
        ),
        migrations.AlterField(
            model_name='computer',
            name='hdd_encrypted',
            field=models.BooleanField(),
        ),
        migrations.AlterField(
            model_name='computer',
            name='os',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Operating System'),
        ),
        migrations.AlterField(
            model_name='computer',
            name='scan_status',
            field=models.IntegerField(choices=[(None, '-- Please choose a value --'), (0, 'Not Yet'), (1, 'Completed')], default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='computer',
            name='updated_at',
            field=django_unixdatetimefield.fields.UnixDateTimeField(blank=True, editable=False, null=True),
        ),
        migrations.AlterField(
            model_name='device',
            name='current_holder',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='current_holder', to='ams.User'),
        ),
        migrations.AlterField(
            model_name='device',
            name='next_holder',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='next_holder', to='ams.User'),
        ),
    ]
