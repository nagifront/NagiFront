import json

from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from .models import UserProfile

# Create your views here.

def index(request):
    return render(request, 'nagifront/layout.html', {
    })

def login(request):
    message = None
    if request.user.is_authenticated():
        if request.method == "POST":
            return JsonResponse({'result': True, 'message': message})
        elif request.method == "GET":
            return redirect('index')

    # With POST request, this view works like API
    if request.method == "POST":
        data = json.loads(request.body.decode())
        username = data.get('id', '')
        password = data.get('password', '')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                django_login(request, user)
                return JsonResponse({'result': True, 'message': message})
            else:
                message = "This user is disabled!"
        else:
            message = "Username or password is invalid."
        return JsonResponse({'result': False, 'message': message})

    return render(request, 'nagifront/login.html', {
        'message' : message
    })

def logout(request):
    django_logout(request)
    return redirect('login')
