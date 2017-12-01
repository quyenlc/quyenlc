from datetime import datetime  
from django.db import connection

from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User, Group

from amsx.models import Location, Manufacturer, Supplier, AssetType, Asset, DHCP
import re


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument(
                '--models', 
                nargs='*', 
                type=str, 
                choices=(
                        'location',
                        'manufacturer',
                        'supplier',
                        'asset_type',
                        'asset',
                        'dhcp'
                    )
            )

    def handle(self, *args, **options):
        def migrate_locations():
            now = datetime.now()

            self.stdout.write(self.style.SUCCESS("Migrating locations"))
            for location in Location.objects.raw('SELECT * from locations'):
                try:
                    amsx_location = Location.objects.get(name__exact = location.name)
                    # self.stdout.write(self.style.WARNING("Update info for user "), ending = ''); self.stdout.write(self.style.SUCCESS(user.username))
                    self.stdout.write(self.style.SUCCESS("Location " + location.name + " existed."))

                except ObjectDoesNotExist as e:
                    self.stdout.write(self.style.WARNING("Location "), ending = ''); self.stdout.write(self.style.SUCCESS(location.name), ending = ''); self.stdout.write(self.style.WARNING(" does not exist. Prepare to create new one ..."))
                    new_location = Location(id = location.id, name=location.name)
                    new_location.save()
            self.stdout.write(self.style.SUCCESS("Finish migrating locations"))
        
        def migrate_manufacturers():
            self.stdout.write(self.style.SUCCESS("Migrating manufacturers"))
            for manufacturer in Manufacturer.objects.raw('SELECT * from manufactures'):
                try:
                    amsx_location = Manufacturer.objects.get(name__exact = manufacturer.name)
                    # self.stdout.write(self.style.WARNING("Update info for user "), ending = ''); self.stdout.write(self.style.SUCCESS(user.username))
                    self.stdout.write(self.style.SUCCESS("Manufacturer " + manufacturer.name + " existed."))

                except ObjectDoesNotExist as e:
                    self.stdout.write(self.style.WARNING("Manufacturer "), ending = ''); self.stdout.write(self.style.SUCCESS(manufacturer.name), ending = ''); self.stdout.write(self.style.WARNING(" does not exist. Prepare to create new one ..."))
                    new_manufacturer = Manufacturer(id = manufacturer.id, name=manufacturer.name)
                    new_manufacturer.save()
            self.stdout.write(self.style.SUCCESS("Finish migrating manufacturers"))

        def migrate_suppliers():
            self.stdout.write(self.style.SUCCESS("Migrating suppliers"))
            for supplier in Supplier.objects.raw('SELECT * from suppliers'):
                try:
                    amsx_supplier = Supplier.objects.get(name__exact = supplier.name)
                    # self.stdout.write(self.style.WARNING("Update info for user "), ending = ''); self.stdout.write(self.style.SUCCESS(user.username))
                    self.stdout.write(self.style.SUCCESS("Supplier " + supplier.name + " existed."))

                except ObjectDoesNotExist as e:
                    self.stdout.write(self.style.WARNING("Supplier "), ending = ''); self.stdout.write(self.style.SUCCESS(supplier.name), ending = ''); self.stdout.write(self.style.WARNING(" does not exist. Prepare to create new one ..."))
                    new_supplier = Supplier(id = supplier.id, name=supplier.name)
                    new_supplier.save()
            self.stdout.write(self.style.SUCCESS("Finish migrating locations"))
        
        def migrate_asset_types():
            self.stdout.write(self.style.SUCCESS("Migrating asset types"))
            for asset_type in AssetType.objects.raw("SELECT id, type FROM `devices` WHERE type != ''"):
                try:
                    amsx_asset_type = AssetType.objects.get(name__exact = asset_type.type)
                    # self.stdout.write(self.style.WARNING("Update info for user "), ending = ''); self.stdout.write(self.style.SUCCESS(user.username))
                    # self.stdout.write(self.style.SUCCESS("Asset Type " + asset_type.type + " existed."))

                except ObjectDoesNotExist as e:
                    self.stdout.write(self.style.WARNING("Asset Type "), ending = ''); self.stdout.write(self.style.SUCCESS(asset_type.type), ending = ''); self.stdout.write(self.style.WARNING(" does not exist. Prepare to create new one ..."))
                    new_asset_type = AssetType(name=asset_type.type)
                    new_asset_type.save()
            self.stdout.write(self.style.SUCCESS("Finish migrating asset types"))

        def migrate_assets():
            self.stdout.write(self.style.SUCCESS("Migrating assets"))
            # Table for AssetType must be truncate before
            for device in Asset.objects.raw("SELECT id, code, type, name, manufacture_id, current_holder, configuration, note, supplier_id, location_id, purchasing_at, warranty_at,status, updated_at FROM devices;"):
                self.stdout.write(self.style.WARNING("Asset "), ending = ''); self.stdout.write(self.style.SUCCESS(device.name), ending = ''); self.stdout.write(self.style.WARNING(" does not exist. Prepare to create new one ..."))
                holder = User.objects.get(id__exact=device.current_holder)
                location = None
                supplier = None
                manufacturer = None
                asset_type = None
                if 0 < device.location_id:
                    location = Location.objects.get(id__exact=device.location_id)

                if 0 < device.supplier_id:
                    supplier = Supplier.objects.get(id__exact=device.supplier_id)

                if 0 < device.manufacture_id:
                    manufacturer = Manufacturer.objects.get(id__exact=device.manufacture_id)                

                if device.type != None:
                    asset_type = AssetType.objects.get(name__exact=device.type)
                    

                new_asset = Asset(
                        id          = device.id, 
                        name        = device.name,
                        old_code    = device.code,
                        holder      = holder,
                        asset_type  = asset_type,
                        description = device.configuration,
                        supplier    = supplier,
                        manufacturer = manufacturer,
                        location    = location,
                        status      = 0,
                        note        = device.note,
                        created_at  = device.updated_at,
                        updated_at  = device.updated_at,
                        purchased_date = device.purchasing_at,
                        availiable_date = device.purchasing_at,
                        warranty_end_date = device.warranty_at
                    )
                try:
                    new_asset.save()
                except Exception as e:
                    print(vars(new_asset))
                    print(e)
                    print(connection.queries[-1])
                    exit()
            self.stdout.write(self.style.SUCCESS("Finish migrating assets")) 
        
        def standardize(mac_addr):
            regex = re.compile(r'[A-Fa-f0-9]+')
            raw_mac_addr = regex.findall(mac_addr)
            if raw_mac_addr == None:
                return mac_addr
            else:
                raw_mac_addr = raw_mac_addr[0].lower()
                return ":".join([raw_mac_addr[i:i+2] for i in range(0,len(raw_mac_addr)-1,2)])


        def migrate_dhcps():
            self.stdout.write(self.style.SUCCESS("Migrating dhcp records"))
            # Table for AssetType must be truncate before
            for record in DHCP.objects.raw("SELECT `id`,`name`,`mac_addr`,`hostname`,`ip_addr`,`device_id` FROM `mac_addresses`"):
                self.stdout.write(self.style.WARNING("Mac Address "), ending = ''); self.stdout.write(self.style.SUCCESS(record.mac_addr), ending = ''); self.stdout.write(self.style.WARNING(" ID:" + str(record.device_id) + " does not exist. Prepare to create new one ..."))
                asset = None
                if 0 < record.device_id:
                    asset = Asset.objects.get(id__exact=record.device_id)
                    
                new_dhcp = DHCP(
                        name        = record.name,
                        mac_addr    = standardize(record.mac_addr),
                        hostname    = record.hostname,
                        ip_addr     = record.ip_addr,
                        asset       = asset,
                    )
                try:
                    new_dhcp.save()
                    # print(new_dhcp.mac_addr)
                except Exception as e:
                    print(e)
                    print(connection.queries[-1])
                    exit()
            self.stdout.write(self.style.SUCCESS("Finish migrating DHCP records")) 

        self.stdout.write(self.style.SUCCESS("Start ..."))
        if not options['models']:
            migrate_locations()
            migrate_manufacturers()
            migrate_suppliers()
            migrate_asset_types()
            migrate_assets()
        else:
            for model in options['models']:
                function_name = 'migrate_' + model + 's'
                possibles = globals().copy()
                possibles.update(locals())
                caller = possibles.get(function_name)
                caller()

        self.stdout.write(self.style.SUCCESS("Finish"))




