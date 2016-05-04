from django.shortcuts import render
from django.http import HttpResponse

from django.contrib.auth.models import User
from .models import UserProfile

# Create your views here.

def index(request):
    return HttpResponse("Hello, world. You're at the nagifront index.")

def login(request):
    # 이미 되어있는가 보기?
    # / 로 리다이렉트
    # 포스트로 처리
    return render(request, 'nagifront/login.html', {
    })
