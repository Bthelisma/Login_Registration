# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from .models import User
from django.contrib import messages
from django.contrib.messages import error

def index(request):
    context = {
        'users': User.objects.all()
    }
    return render(request, "login/index.html", context)


def register(request):
    result = User.objects.register_validate(request.POST)
    if type(result) == list:
        for error in result:
            messages.error(request, error)
        return redirect('/')
    request.session['user_id']= result.id
    messages.success(request, "Successfully registered!")
    return redirect('/success')


def login(request):
    result= User.objects.login_validate(request.POST)
    if type(result) == list:
        for error in result:
            messages.error(request, error)
    # if 'user_id' not in request.session:
        return redirect ("/")
    request.session['user_id']= result.id
    messages.success(request, "Successfully logged in!")
    return redirect("/success")


def success(request):
    try:
        request.session['user_id']
    except KeyError:
        return redirect('/')
    context = {
        'user': User.objects.get(id=request.session['user_id'])
    }
    return render (request, "login/success.html", context)
