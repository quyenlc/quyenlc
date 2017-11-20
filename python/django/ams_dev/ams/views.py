# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def test(request):
    current_user = request.user
    return HttpResponse("Hello " + current_user.username)

def fail_login(request):
    return HttpResponse("Á hự! Đek đăng nhập được rồi")
