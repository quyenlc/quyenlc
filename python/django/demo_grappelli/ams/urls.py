from django.conf.urls import url

from . import views

urlpatterns = [
    # ex: /ams/
    url(r'^', views.list_devices, name='list_devices'),
    url(r'^login', views.login, name='login'),
    url(r'^logout', views.logout, name='logout'),
]