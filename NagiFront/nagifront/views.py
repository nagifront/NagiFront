from django.shortcuts import render
from django.http import HttpResponse

from django.contrib.auth.models import User
from .models import UserProfile

# Create your views here.

def index(request):
    return HttpResponse("Hello, world. You're at the nagifront index.")

