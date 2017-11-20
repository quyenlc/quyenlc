from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^test', views.test, name='test'),
    url(r'^$', views.idol_index, name='idol_index'),
]
