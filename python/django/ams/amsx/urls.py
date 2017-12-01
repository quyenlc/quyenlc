from django.conf.urls import include, url
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'test', views.test, name='test'),
    url(r'assets', views.my_asset, name='my_asset'),
]
