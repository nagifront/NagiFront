import json

from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as django_login

from .models import UserProfile
from .nagios_models import *

# Create your views here.

def index(request):
    return HttpResponse("Hello, world. You're at the nagifront index.")

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

@login_required
def hosts_overall(request):
    if request.method == 'GET':
        # Get the number of hosts and the number of hosts in 'up' state.
        hosts_num = NagiosHoststatus.objects.count()
        up_hosts_num = len(NagiosHoststatus.objects.filter(current_state=0))

        warning_host_set = set()
        critical_host_set = set()
        unknown_host_set = set()

        # Get (service_object_id,  current_state) from NagiosServiceStatus,
        #     (service_object_id, host_object_id) from NagiosServices.
        #
        # Note that states of these services are one of { warning, critical, unknown }.
        unusual_service_state_lists = NagiosServicestatus.objects.filter(current_state__gte=1).values_list('service_object_id', 'current_state')
        unusual_service_host_lists = NagiosServices.objects.filter(service_object_id__in=[s_id for s_id, state in unusual_service_state_lists]).values_list('service_object_id', 'host_object_id')

        # Classify these services by state, and put their host ids into corresponding set.
        service_to_host = dict(unusual_service_host_lists)
        for s_id, state in unusual_service_state_lists:
            if state == 1:
                warning_host_set.add(service_to_host[s_id])
            elif state == 2:
                critical_host_set.add(service_to_host[s_id])
            else:
                unknown_host_set.add(service_to_host[s_id])

        return JsonResponse({'all':hosts_num, 'up':up_hosts_num, 'warning':len(warning_host_set), 'critical':len(critical_host_set)})
