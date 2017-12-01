# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class AssetType(models.Model):
    name                = models.CharField(verbose_name="Asset type",max_length =100)
    is_kitting_required = models.BooleanField()
    def __unicode__(self):
       return self.name

class Supplier(models.Model):
    name    = models.CharField(max_length =100)
    contact = models.TextField()
    def __unicode__(self):
       return self.name

class Manufacturer(models.Model):
    name = models.CharField(max_length =100)
    def __unicode__(self):
       return self.name
            
class Location(models.Model):
    name = models.CharField(max_length =100)
    description = models.TextField()
    def __unicode__(self):
       return self.name      

class Asset(models.Model):
    old_code = models.CharField(max_length =100)
    name = models.CharField(max_length =100)
    holder = models.ForeignKey('auth.User', default=None)
    group_holder = models.ForeignKey('auth.Group', default=None)
    asset_type = models.ForeignKey('AssetType')
    description = models.TextField()
    supplier = models.ForeignKey('Supplier', default=None)
    manufacturer = models.ForeignKey('Manufacturer', default=None)
    location = models.ForeignKey('Location', default=None)
    purchased_date = models.DateTimeField(auto_now_add=True)
    availiable_date = models.DateTimeField()
    warranty_start_date = models.DateTimeField()
    warranty_end_date = models.DateTimeField()
    status = models.IntegerField()
    image_url = models.CharField(max_length=256)
    note = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def getHolder(self):
        return self.holder.username
    getHolder.short_description = 'Holder'
    getHolder.admin_order_field = 'holder__username'

    def getAssetType(self):
        return self.asset_type.name
    getAssetType.short_description = 'Type'
    getAssetType.admin_order_field = 'asset_type__name'

    def getSupplier(self):
        return self.supplier.name
    getSupplier.short_description = 'Supplier'
    getSupplier.admin_order_field = 'supplier__name'


    def getManufacturer(self):
        return self.manufacturer.name
    getManufacturer.short_description = 'Manufacturer'
    getManufacturer.admin_order_field = 'manufacturer__name'

    def getLocation(self):
        return self.location.name
    getLocation.short_description = 'Location'
    getLocation.admin_order_field = 'location__name'


    def __unicode__(self):
       return self.name

class DHCP(models.Model):
    asset       = models.ForeignKey('Asset', null=True)
    name        = models.CharField(max_length=100, null=True,verbose_name='Interface Name')
    mac_addr    = models.CharField(max_length=100)
    hostname    = models.CharField(max_length=100, null=True)
    ip_addr     = models.GenericIPAddressField(null=True)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    def getAssetName(self):
        if self.asset != None:
            return self.asset.name
        else:
            return '-'
    getAssetName.short_description = 'Asset Name'
    getAssetName.admin_order_field = 'asset__name'

    def __unicode__(self):
        return self.mac_addr


        






        

