from django.contrib import admin
from django.contrib.admin import AdminSite
from django.contrib.auth.models import User, Group

# Register your models here.
from .models import Location, Manufacture, Platform, Supplier, Device, User as OldUser, Computer
"""https://docs.djangoproject.com/en/1.11/ref/contrib/admin/"""
class MyAdminSite(AdminSite):
    login_template = 'backend/login.html'
    site_header = "Punch Asset Manager"

backend = MyAdminSite(name='backend')

class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'first_name', 'last_name', 'email','is_superuser','is_staff', 'is_active')
backend.register(User, UserAdmin)

backend.register(Group)

backend.register(Location)
backend.register(Manufacture)
backend.register(Platform)
backend.register(Supplier)

class ComputerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'getDeviceName', 'getHolder')
backend.register(Computer, ComputerAdmin)

