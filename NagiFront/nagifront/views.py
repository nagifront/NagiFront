from django.shortcuts import render, redirect
from django.http import HttpResponse

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as django_login
from .models import UserProfile

# Create your views here.

def index(request):
    return HttpResponse("Hello, world. You're at the nagifront index.")

def login(request):
    message = None
    if request.user.is_authenticated():
        return redirect('index')

    if request.method == "POST":
        username = request.POST['id']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                django_login(request, user)
                return redirect('index')
            else:
                message = "This user is disabled!"
        else:
            message = "Username or password is invalid."

    return render(request, 'nagifront/login.html', {
        'message' : message
    })
