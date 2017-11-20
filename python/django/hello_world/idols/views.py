# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Idol
from .forms import IdolSearchForm 

# Create your views here.
def test(request):
    return HttpResponse("Hello, world. You're at the idols/test.")
def idol_index(request):
    if 'name' in request.GET:
        name = request.GET['name']
        idols = Idol.objects.filter(name__contains=name)
    else:
        name = ''
        idols = Idol.objects.all()
    if 'year_of_birth' in request.GET and request.GET['year_of_birth'].isdigit():
        year_of_birth = request.GET['year_of_birth']
        idols = idols.filter(birthday__year=year_of_birth)
    else:
        year_of_birth = 0
    
    if year_of_birth == 0:
        form = IdolSearchForm(initial={'name': name})
    else:
        form = IdolSearchForm(initial={'name': name, 'year_of_birth': year_of_birth})
    template = loader.get_template('idols/index.html')
    context = {
        'idols': idols,
        'form' : form,
    }
    return HttpResponse(template.render(context, request))
