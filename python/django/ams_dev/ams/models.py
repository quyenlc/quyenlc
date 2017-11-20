# -*- coding: utf-8 -*-
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin sqlcustom [app_label]'
# into your database.
from __future__ import unicode_literals

from django.db import models
from django_unixdatetimefield.fields import UnixDateTimeField



class ComputerSoftwares(models.Model):
    device = models.ForeignKey('Device')
    software = models.IntegerField()
    status = models.IntegerField()
    modified = models.DateTimeField(blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'computer_softwares'


class Computer(models.Model):

    # for has-choices-fields.
    AUTO_CHOICES = (
           (None, '-- Please choose a value --'),
           (0, 'Automatic'),
           (1, 'Manually'),
        )

    SCAN_STATUS_CHOICES  = (
            (None, '-- Please choose a value --'),
            (0,'Not Yet'),
            (1, 'Completed'),
        )

    device              = models.ForeignKey('Device')
    name                = models.CharField(unique=True, max_length=20)
    os                  = models.CharField(max_length=50, blank=True, null=True, verbose_name='Operating System')
    hdd_encrypted       = models.BooleanField()
    ad_binding          = models.BooleanField()
    av_software         = models.CharField(max_length=100, blank=True, null=True, verbose_name = 'Antivirus(AV) Software')
    av_version          = models.CharField(max_length=20, blank=True, null=True, verbose_name = 'Version of AV software')
    safe_av_version     = models.CharField(max_length=64, blank=True, null=True, verbose_name = "Safe Version for AV Software")
    pattern_date        = models.CharField(max_length=64, blank=True, null=True)
    safe_pattern_date   = models.CharField(max_length=64, blank=True, null=True)
    fde_software        = models.CharField(max_length=100, blank=True, null=True, verbose_name = 'Full-Disk Encryption(FDE) Software')
    fde_version         = models.CharField(max_length=20, blank=True, null=True, verbose_name = 'Version of FDE software')
    note                = models.TextField(blank=True, null=True)
    created_at          = UnixDateTimeField(blank=True, null=True, editable=False)
    updated_at          = UnixDateTimeField(blank=True, null=True, editable=False)
    auto                = models.IntegerField(choices=AUTO_CHOICES, editable=False)
    scan_status         = models.IntegerField(choices=SCAN_STATUS_CHOICES)

    class Meta:
        db_table = 'computers'

    def __unicode__(self):
        return self.name or u''

    def getDeviceName(self):
        return self.device.name
    getDeviceName.short_description = 'Device Name'

    def getHolder(self):
        return self.device.current_holder.username
    getHolder.short_description = 'Holder'


class Config(models.Model):
    key = models.CharField(max_length=20)
    value = models.TextField()
    description = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'configs'


class Constant(models.Model):
    key = models.CharField(max_length=50)
    value = models.CharField(max_length=20)
    text = models.CharField(max_length=50)

    class Meta:
        db_table = 'constants'
        unique_together = (('key', 'value'),)


class DeviceChangeLog(models.Model):
    device = models.IntegerField()
    user = models.IntegerField()
    field_name = models.CharField(max_length=20)
    old_value = models.CharField(max_length=200, blank=True, null=True)
    new_value = models.CharField(max_length=200, blank=True, null=True)
    updated_at = models.DateTimeField()

    class Meta:
        db_table = 'device_change_logs'


class Device(models.Model):
    code = models.CharField(max_length=15, blank=True, null=True)
    device_type = models.CharField(max_length=20, blank=True, null=True, db_column = 'type')
    name = models.CharField(max_length=100, blank=True, null=True)
    manufacture = models.ForeignKey('Manufacture')
    platform = models.ForeignKey('Platform')
    identification_code = models.CharField(max_length=30, blank=True, null=True)
    purchasing_at = models.DateField(blank=True, null=True)
    warranty_at = models.DateField(blank=True, null=True)
    activated_at = models.DateField(blank=True, null=True)
    used_at = models.DateField(blank=True, null=True)
    validity_day = models.IntegerField(blank=True, null=True)
    version = models.CharField(max_length=30, blank=True, null=True)
    configuration = models.TextField(blank=True, null=True)
    location = models.ForeignKey('Location')
    supplier = models.ForeignKey('Supplier')
    purpose = models.CharField(max_length=11, blank=True, null=True)
    current_holder = models.ForeignKey('User', related_name = 'current_holder')
    status = models.CharField(max_length=20, blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    cost = models.IntegerField(blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    pv_number = models.CharField(max_length=20, blank=True, null=True)
    eligibility12 = models.DateField(blank=True, null=True)
    eligibility21 = models.DateField(blank=True, null=True)
    flag = models.IntegerField(blank=True, null=True)
    new = models.IntegerField(blank=True, null=True)
    next_holder = models.ForeignKey('User', related_name = 'next_holder')
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'devices'

    def __unicode__(self):
        return self.name or u''


class History(models.Model):
    from_user = models.ForeignKey('User', related_name = 'old_holder')
    to_user = models.ForeignKey('User', related_name = 'new_holder')
    item = models.ForeignKey('Device')
    item_code = models.CharField(max_length=20, blank=True, null=True)
    reason = models.CharField(max_length=20, blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    hand_at = models.IntegerField(blank=True, null=True)
    take_at = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'histories'


class Inuses(models.Model):
    computer = models.ForeignKey('Computer')
    license = models.ForeignKey('License')
    flag = models.IntegerField(blank=True, null=True)
    created_at = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'inuses'


class LicenseSoftware(models.Model):
    software = models.ForeignKey('Software')
    license = models.ForeignKey('License')
    key_type = models.IntegerField(blank=True, null=True)
    product_key = models.CharField(max_length=128)
    note = models.TextField()
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'license_softwares'


class License(models.Model):
    software_group = models.ForeignKey('SoftwareGroup')
    name = models.CharField(max_length=128)
    num = models.IntegerField()
    used_num = models.IntegerField()
    computers_per_lic = models.IntegerField()
    renew_required = models.SmallIntegerField()
    agreement_number = models.CharField(max_length=128, blank=True, null=True)
    purchased_at = models.DateField(blank=True, null=True)
    expired_at = models.DateField(blank=True, null=True)
    ver_win_min = models.CharField(max_length=16, blank=True, null=True)
    ver_win_max = models.CharField(max_length=16, blank=True, null=True)
    ver_mac_min = models.CharField(max_length=16, blank=True, null=True)
    ver_mac_max = models.CharField(max_length=16, blank=True, null=True)
    note = models.TextField()
    created = models.DateTimeField()
    modified = models.DateTimeField()

    class Meta:
        db_table = 'licenses'

    def __unicode__(self):
        return self.name or u''


class Location(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        db_table = 'locations'

    def __unicode__(self):
        return self.name or u''


class MacAddress(models.Model):
    device = models.ForeignKey('Device')
    name = models.TextField()
    mac_addr = models.CharField(unique=True, max_length=20)
    ip_addr = models.CharField(max_length=200, blank=True, null=True)
    created_at = models.IntegerField(blank=True, null=True)
    updated_at = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'mac_addresses'

    def __unicode__(self):
        return self.mac_addr or u''


class Manufacture(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        db_table = 'manufactures'

    def __unicode__(self):
        return self.name or u''


class Platform(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        db_table = 'platforms'

    def __unicode__(self):
        return self.name or u''


class SoftwareGroup(models.Model):
    name = models.CharField(max_length=128)
    platform = models.IntegerField(blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'software_groups'


class Software(models.Model):
    software_group = models.ForeignKey('SoftwareGroup')
    name = models.CharField(max_length=128)
    alias = models.CharField(max_length=128)
    version = models.CharField(max_length=128, blank=True, null=True)
    platform = models.ForeignKey('Platform')
    software_type = models.IntegerField()
    category = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'softwares'


class Supplier(models.Model):
    name = models.CharField(max_length=150, blank=True, null=True)

    class Meta:
        db_table = 'suppliers'

    def __unicode__(self):
        return self.name or u''


class UserSoftware(models.Model):
    user = models.ForeignKey('User')
    license = models.ForeignKey('License')
    license_software = models.ForeignKey('LicenseSoftware')
    num_of_license = models.IntegerField()
    status = models.IntegerField()
    note = models.TextField()
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'user_softwares'


class User(models.Model):
    username = models.CharField(unique=True, max_length=50, blank=True, null=True)
    role = models.CharField(max_length=20, blank=True, null=True)
    full_name = models.CharField(max_length=70, blank=True, null=True)
    password = models.CharField(max_length=50, blank=True, null=True)
    flag = models.IntegerField(blank=True, null=True)
    email = models.CharField(max_length=30, blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    skype_id = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'users'

    def __unicode__(self):
        return self.full_name or u''


class ADComputer(models.Model):
    """docstring for ADComputer"""
    email       = models.CharField(max_length=200)
    name        = models.CharField(unique=True, max_length=50)
    fde_software= models.CharField(max_length=200)
    os          = models.CharField(max_length=50)
    fde_status  = models.IntegerField(default=-1)
    scan_status = models.IntegerField(default=-1)
    note = models.TextField(blank=True, default='')

    def __unicode__(self):
        return self.full_name or u''

    def getOSPlatform(self):
        if ('-win' in self.name.lower()):
            return 'Win'
        elif '-mac' in self.name.lower():
            return 'Mac'
        else:
            return 'Others'

    def getIP(self):
        dhcp_info = list(DHCP.objects.filter(hostname__icontains=self.name).order_by('ip_addr').values('ip_addr','mac_addr'))
        if len(dhcp_info) != 0:
            return dhcp_info
        else:
            return None


class DHCP(models.Model):
    """docstring for DHCP"""

    mac_addr = models.CharField(max_length=32)
    device_id = models.IntegerField(default=0)
    ip_addr     =  models.CharField(max_length=64)
    hostname = models.CharField(max_length=64)
    created_at = UnixDateTimeField(editable = False)
    updated_at = UnixDateTimeField(editable = False)
        


        