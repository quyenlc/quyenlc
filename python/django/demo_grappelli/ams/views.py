# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout

from .forms import LoginForm

# Create your views here.
def index(request):
    template = loader.get_template('ams/index.html')

    context = {
        'user': request.user
    }
    return HttpResponse(template.render(context, request))

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        user_login = form.login()
        if user_login is not None:
            auth_login(request, user_login)
            return HttpResponseRedirect('/')
        else:
            form.add_error(None, "Username or password is incorrect. Please try again")
    else:
        form = LoginForm()

    return render(request, 'ams/login.html', {'form': form})

def logout(request):
    auth_logout(request)
    return HttpResponseRedirect('/')

def list_devices(request):
    template = loader.get_template('ams/devices/index.html')

    context = {
    }
    return HttpResponse(template.render(context, request))
