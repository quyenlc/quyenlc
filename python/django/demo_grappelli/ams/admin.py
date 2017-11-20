# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Manufacture, DeviceType, Platform, Platform, Location, Supplier

# Register your models here.
admin.site.register(Manufacture)
admin.site.register(DeviceType)
admin.site.register(Platform)
admin.site.register(Location)
admin.site.register(Supplier)