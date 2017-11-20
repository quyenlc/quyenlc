# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Computer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=20)),
                ('os', models.CharField(max_length=50, null=True, blank=True)),
                ('hdd_encrypted', models.IntegerField()),
                ('ad_binding', models.IntegerField()),
                ('antivirus_software', models.CharField(max_length=100, null=True, blank=True)),
                ('antivirus_ver', models.CharField(max_length=20, null=True, blank=True)),
                ('fde_software', models.CharField(max_length=100, null=True, blank=True)),
                ('fde_ver', models.CharField(max_length=20, null=True, blank=True)),
                ('note', models.TextField(null=True, blank=True)),
                ('created_at', models.IntegerField(null=True, blank=True)),
                ('updated_at', models.IntegerField(null=True, blank=True)),
                ('auto', models.IntegerField()),
                ('orange_status', models.CharField(max_length=200, null=True, blank=True)),
                ('orange_version', models.CharField(max_length=64, null=True, blank=True)),
                ('av_safe_version', models.CharField(max_length=64, null=True, blank=True)),
                ('pattern_date', models.CharField(max_length=64, null=True, blank=True)),
                ('av_safe_pattern_date', models.CharField(max_length=64, null=True, blank=True)),
                ('scan_status', models.IntegerField(null=True, blank=True)),
            ],
            options={
                'db_table': 'computers',
            },
        ),
        migrations.CreateModel(
            name='ComputerSoftwares',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('software_id', models.IntegerField()),
                ('status', models.IntegerField()),
                ('modified', models.DateTimeField(null=True, blank=True)),
                ('created', models.DateTimeField(null=True, blank=True)),
            ],
            options={
                'db_table': 'computer_softwares',
            },
        ),
        migrations.CreateModel(
            name='Config',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('key', models.CharField(max_length=20)),
                ('value', models.TextField()),
                ('description', models.TextField(null=True, blank=True)),
            ],
            options={
                'db_table': 'configs',
            },
        ),
        migrations.CreateModel(
            name='Constant',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('key', models.CharField(max_length=50)),
                ('value', models.CharField(max_length=20)),
                ('text', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'constants',
            },
        ),
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(max_length=15, null=True, blank=True)),
                ('type', models.CharField(max_length=20, null=True, blank=True)),
                ('name', models.CharField(max_length=100, null=True, blank=True)),
                ('identification_code', models.CharField(max_length=30, null=True, blank=True)),
                ('purchasing_at', models.DateField(null=True, blank=True)),
                ('warranty_at', models.DateField(null=True, blank=True)),
                ('activated_at', models.DateField(null=True, blank=True)),
                ('used_at', models.DateField(null=True, blank=True)),
                ('validity_day', models.IntegerField(null=True, blank=True)),
                ('version', models.CharField(max_length=30, null=True, blank=True)),
                ('configuration', models.TextField(null=True, blank=True)),
                ('purpose', models.CharField(max_length=11, null=True, blank=True)),
                ('current_holder', models.IntegerField(null=True, blank=True)),
                ('status', models.CharField(max_length=20, null=True, blank=True)),
                ('note', models.TextField(null=True, blank=True)),
                ('cost', models.IntegerField(null=True, blank=True)),
                ('phone_number', models.CharField(max_length=15, null=True, blank=True)),
                ('pv_number', models.CharField(max_length=20, null=True, blank=True)),
                ('eligibility12', models.DateField(null=True, blank=True)),
                ('eligibility21', models.DateField(null=True, blank=True)),
                ('flag', models.IntegerField(null=True, blank=True)),
                ('new', models.IntegerField(null=True, blank=True)),
                ('updated_at', models.DateTimeField(null=True, blank=True)),
            ],
            options={
                'db_table': 'devices',
            },
        ),
        migrations.CreateModel(
            name='DeviceChangeLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('device_id', models.IntegerField()),
                ('user_id', models.IntegerField()),
                ('field_name', models.CharField(max_length=20)),
                ('old_value', models.CharField(max_length=200, null=True, blank=True)),
                ('new_value', models.CharField(max_length=200, null=True, blank=True)),
                ('updated_at', models.DateTimeField()),
            ],
            options={
                'db_table': 'device_change_logs',
            },
        ),
        migrations.CreateModel(
            name='History',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('item_code', models.CharField(max_length=20, null=True, blank=True)),
                ('reason', models.CharField(max_length=20, null=True, blank=True)),
                ('status', models.IntegerField(null=True, blank=True)),
                ('comment', models.TextField(null=True, blank=True)),
                ('hand_at', models.IntegerField(null=True, blank=True)),
                ('take_at', models.IntegerField(null=True, blank=True)),
            ],
            options={
                'db_table': 'histories',
            },
        ),
        migrations.CreateModel(
            name='Inuses',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('flag', models.IntegerField(null=True, blank=True)),
                ('created_at', models.IntegerField(null=True, blank=True)),
                ('computer_id', models.ForeignKey(to='ams.Computer')),
            ],
            options={
                'db_table': 'inuses',
            },
        ),
        migrations.CreateModel(
            name='License',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128)),
                ('num', models.IntegerField()),
                ('used_num', models.IntegerField()),
                ('computers_per_lic', models.IntegerField()),
                ('renew_required', models.SmallIntegerField()),
                ('agreement_number', models.CharField(max_length=128, null=True, blank=True)),
                ('purchased_at', models.DateField(null=True, blank=True)),
                ('expired_at', models.DateField(null=True, blank=True)),
                ('ver_win_min', models.CharField(max_length=16, null=True, blank=True)),
                ('ver_win_max', models.CharField(max_length=16, null=True, blank=True)),
                ('ver_mac_min', models.CharField(max_length=16, null=True, blank=True)),
                ('ver_mac_max', models.CharField(max_length=16, null=True, blank=True)),
                ('note', models.TextField()),
                ('created', models.DateTimeField()),
                ('modified', models.DateTimeField()),
            ],
            options={
                'db_table': 'licenses',
            },
        ),
        migrations.CreateModel(
            name='LicenseSoftware',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('key_type', models.IntegerField(null=True, blank=True)),
                ('product_key', models.CharField(max_length=128)),
                ('note', models.TextField()),
                ('created', models.DateTimeField(null=True, blank=True)),
                ('modified', models.DateTimeField(null=True, blank=True)),
                ('license_id', models.ForeignKey(to='ams.License')),
            ],
            options={
                'db_table': 'license_softwares',
            },
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50, null=True, blank=True)),
            ],
            options={
                'db_table': 'locations',
            },
        ),
        migrations.CreateModel(
            name='MacAddress',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.TextField()),
                ('mac_addr', models.CharField(unique=True, max_length=20)),
                ('ip_addr', models.CharField(max_length=200, null=True, blank=True)),
                ('created_at', models.IntegerField(null=True, blank=True)),
                ('updated_at', models.IntegerField(null=True, blank=True)),
                ('device_id', models.ForeignKey(to='ams.Device')),
            ],
            options={
                'db_table': 'mac_addresses',
            },
        ),
        migrations.CreateModel(
            name='Manufacture',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50, null=True, blank=True)),
            ],
            options={
                'db_table': 'manufactures',
            },
        ),
        migrations.CreateModel(
            name='Platform',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50, null=True, blank=True)),
            ],
            options={
                'db_table': 'platforms',
            },
        ),
        migrations.CreateModel(
            name='Software',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128)),
                ('alias', models.CharField(max_length=128)),
                ('version', models.CharField(max_length=128, null=True, blank=True)),
                ('type', models.IntegerField()),
                ('category', models.IntegerField()),
                ('created', models.DateTimeField(null=True, blank=True)),
                ('modified', models.DateTimeField(null=True, blank=True)),
                ('platform', models.ForeignKey(to='ams.Platform')),
            ],
            options={
                'db_table': 'softwares',
            },
        ),
        migrations.CreateModel(
            name='SoftwareGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128)),
                ('platform', models.IntegerField(null=True, blank=True)),
                ('created', models.DateTimeField(null=True, blank=True)),
                ('modified', models.DateTimeField(null=True, blank=True)),
            ],
            options={
                'db_table': 'software_groups',
            },
        ),
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=150, null=True, blank=True)),
            ],
            options={
                'db_table': 'suppliers',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('username', models.CharField(max_length=50, unique=True, null=True, blank=True)),
                ('role', models.CharField(max_length=20, null=True, blank=True)),
                ('full_name', models.CharField(max_length=70, null=True, blank=True)),
                ('password', models.CharField(max_length=50, null=True, blank=True)),
                ('flag', models.IntegerField(null=True, blank=True)),
                ('email', models.CharField(max_length=30, null=True, blank=True)),
                ('created', models.DateTimeField(null=True, blank=True)),
                ('modified', models.DateTimeField(null=True, blank=True)),
                ('skype_id', models.IntegerField(null=True, blank=True)),
            ],
            options={
                'db_table': 'users',
            },
        ),
        migrations.CreateModel(
            name='UserSoftware',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('num_of_license', models.IntegerField()),
                ('status', models.IntegerField()),
                ('note', models.TextField()),
                ('created', models.DateTimeField(null=True, blank=True)),
                ('modified', models.DateTimeField(null=True, blank=True)),
                ('license_id', models.ForeignKey(to='ams.License')),
                ('license_software_id', models.ForeignKey(to='ams.LicenseSoftware')),
                ('user_id', models.ForeignKey(to='ams.User')),
            ],
            options={
                'db_table': 'user_softwares',
            },
        ),
        migrations.AddField(
            model_name='software',
            name='software_group_id',
            field=models.ForeignKey(to='ams.SoftwareGroup'),
        ),
        migrations.AddField(
            model_name='licensesoftware',
            name='software_id',
            field=models.ForeignKey(to='ams.Software'),
        ),
        migrations.AddField(
            model_name='license',
            name='software_group_id',
            field=models.ForeignKey(to='ams.SoftwareGroup'),
        ),
        migrations.AddField(
            model_name='inuses',
            name='license_id',
            field=models.ForeignKey(to='ams.License'),
        ),
        migrations.AddField(
            model_name='history',
            name='from_user_id',
            field=models.ForeignKey(related_name='old_holder', to='ams.User'),
        ),
        migrations.AddField(
            model_name='history',
            name='item_id',
            field=models.ForeignKey(to='ams.Device'),
        ),
        migrations.AddField(
            model_name='history',
            name='to_user_id',
            field=models.ForeignKey(related_name='new_holder', to='ams.User'),
        ),
        migrations.AddField(
            model_name='device',
            name='location_id',
            field=models.ForeignKey(to='ams.Location'),
        ),
        migrations.AddField(
            model_name='device',
            name='manufacture_id',
            field=models.ForeignKey(to='ams.Manufacture'),
        ),
        migrations.AddField(
            model_name='device',
            name='next_holder',
            field=models.ForeignKey(to='ams.User'),
        ),
        migrations.AddField(
            model_name='device',
            name='platform',
            field=models.ForeignKey(to='ams.Platform'),
        ),
        migrations.AddField(
            model_name='device',
            name='supplier_id',
            field=models.ForeignKey(to='ams.Supplier'),
        ),
        migrations.AlterUniqueTogether(
            name='constant',
            unique_together=set([('key', 'value')]),
        ),
        migrations.AddField(
            model_name='computersoftwares',
            name='device_id',
            field=models.ForeignKey(to='ams.Device'),
        ),
        migrations.AddField(
            model_name='computer',
            name='device_id',
            field=models.ForeignKey(to='ams.Device'),
        ),
    ]
