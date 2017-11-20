# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Manufacture(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class DeviceType(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class Platform(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class Location(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class Supplier(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class Device(models.Model):
    code                = models.CharField(max_length=15)
    classification      = models.ForeignKey('DeviceType', on_delete=models.PROTECT)
    name                = models.CharField(max_length=100)
    manufacture         = models.ForeignKey('Manufacture', on_delete=models.PROTECT)
    platform            = models.ForeignKey('Platform', on_delete=models.PROTECT)
    identification_code = models.CharField(max_length=30)
    purchasing_at       = models.DateTimeField(blank=True)
    warranty_at         = models.DateTimeField(blank=True)
    activated_at        = models.DateTimeField(blank=True)
    used_at             = models.DateTimeField(blank=True)
    validity_day        = models.IntegerField(blank=True)
    version             = models.CharField(max_length=30, blank=True)
    configuration       = models.TextField(blank=True)
    location            = models.ForeignKey('Location', on_delete=models.PROTECT)
    supplier            = models.ForeignKey('Supplier', on_delete=models.PROTECT)
    purpose             = models.CharField(max_length=11, blank=True)
    current_holder      = models.ForeignKey(User, on_delete=models.PROTECT, related_name='current_holder')
    status              = models.CharField(max_length=20, blank=True)
    note                = models.TextField(blank=True)
    cost                = models.IntegerField(blank=True)
    phone_number        = models.CharField(max_length=15, blank=True)
    pv_number           = models.CharField(max_length=20, blank=True)
    eligibility12       = models.DateTimeField(blank=True)
    eligibility21       = models.DateTimeField(blank=True)
    flag                = models.IntegerField(blank=True)
    new                 = models.IntegerField(blank= True)
    next_holder         = models.ForeignKey(User, on_delete=models.PROTECT, related_name='next_holder')
    updated_at          = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


