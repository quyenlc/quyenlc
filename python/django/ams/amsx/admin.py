# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from amsx.models import *

# Register your models here.
class AssetTypeAdmin(admin.ModelAdmin):
    list_display = ('id','name','is_kitting_required')
    list_filter = ('is_kitting_required',)

class LocationAdmin(admin.ModelAdmin):
    list_display = ('id','name','description')

class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ('id','name')

class SupplierAdmin(admin.ModelAdmin):
    list_display = ('id','name','contact')

class AssetAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'getAssetType', 'getHolder', 'getSupplier', 'getManufacturer', 'getLocation')
    list_filter = ('asset_type__name', 'holder__username','location__name')
    search_fields = ['id','name','asset_type__name', 'holder__username','location__name']

class DhcpAdmin(admin.ModelAdmin):
    list_display = ('mac_addr','ip_addr','hostname', 'getAssetName','name','updated_at')
    search_fields = ('name','mac_addr','ip_addr','hostname', 'asset__name')

admin.site.register(Manufacturer, ManufacturerAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(AssetType, AssetTypeAdmin)
admin.site.register(Supplier, SupplierAdmin)
admin.site.register(Asset, AssetAdmin)
admin.site.register(DHCP, DhcpAdmin)




