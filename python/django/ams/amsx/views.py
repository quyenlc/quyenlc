# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from .models import Asset
from django.template import loader

# Create your views here.
def test(request):
    return HttpResponse("Test is done")

def my_asset(request):
    template = loader.get_template('assets/index.html')
    if request.user.is_authenticated():
        my_id = request.user.id
        print(my_id)
        assets = Asset.objects.filter(holder_id = my_id)
        print(assets)
        context = {
                'assets': assets,
            }
        return HttpResponse(template.render(context, request))
    else:
        return HttpResponse("You are not loged in")