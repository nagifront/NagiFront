from django.shortcuts import render
from django.http import HttpResponse

from django.contrib.auth.models import User
from .models import UserProfile

# Create your views here.

def index(request):
    return HttpResponse("Hello, world. You're at the nagifront index.")

# Test view for check dashboard setting functionality.
def show_dashboard_setting(request, user_id):
    selected_user = User.objects.get(pk=user_id)
    context = {"selected_user_dashboard_setting": selected_user.userprofile.dashboard_setting }
    return render(request, 'nagifront/dashboard_setting.html', context)

