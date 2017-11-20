from django.contrib import admin

# Register your models here.
from .models import Location, Manufacture, Platform, Supplier, Device, User, Computer

admin.site.register(Location)
admin.site.register(Manufacture)
admin.site.register(Platform)
admin.site.register(Supplier)

class ComputerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'getDeviceName', 'getHolder')
admin.site.register(Computer, ComputerAdmin)

