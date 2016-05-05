import json

from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as django_login

from django.core.exceptions import ObjectDoesNotExist

from django.db.models import Count
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

        # Introduce priority between warning and critical
        # Now, in warning_host_set, only exist hosts (having 'warning' services && !having 'critical' services)
        warning_host_set = warning_host_set - critical_host_set

        return JsonResponse({'all':hosts_num, 'up':up_hosts_num, 'warning':len(warning_host_set), 'critical':len(critical_host_set)})

@login_required
def hosts_groups(request):
    # Get member and alias data about group_obj_id
    def host_group_helper(group_obj_id):
        hostgroup = NagiosHostgroups.objects.get(hostgroup_object_id=group_obj_id)
        alias = hostgroup.alias
        members = NagiosHostgroupMembers.objects.filter(hostgroup_id=hostgroup.hostgroup_id).values_list('host_object_id', flat=True)
        return dict(members=list(members), alias=alias)

    if request.method == 'GET':
        try:
            result = dict()
            group_obj_id = request.GET.get('host_group_id')
            if group_obj_id is not None:
                result[str(group_obj_id)] = host_group_helper(group_obj_id)
            else:
                group_obj_id_list = NagiosHostgroups.objects.all().values_list('hostgroup_object_id', flat=True)
                for group_obj_id in group_obj_id_list:
                    result[str(group_obj_id)] = host_group_helper(group_obj_id)

            return JsonResponse(result)
        except ObjectDoesNotExist:
            return JsonResponse(dict())

@login_required
def hosts_groups_service_number_by_state(request):
    # Get alias and service statistics about group_obj_id
    def host_group_services_helper(group_obj_id):
        hostgroup = NagiosHostgroups.objects.get(hostgroup_object_id=group_obj_id)
        alias = hostgroup.alias
        members = NagiosHostgroupMembers.objects.filter(hostgroup_id=hostgroup.hostgroup_id).values_list('host_object_id', flat=True)
        services = NagiosServices.objects.filter(host_object_id__in=members).values_list('service_object_id', flat=True)
        
        # From NagiosServicestatus, get services belong to selected hostgroup, group by current state, 
        # count it, sort it, list-ify count results and fill trailing zeros.
        services_state_count = list(NagiosServicestatus.objects.filter(service_object_id__in=services).values('current_state').annotate(Count('current_state')).order_by('current_state').values_list('current_state__count', flat=True)) + [0, 0, 0, 0]
        
        return {'alias':alias, 'Ok':services_state_count[0], 'Warning':services_state_count[1], 'Critical':services_state_count[2], 'Unknown':services_state_count[3]}

    if request.method == 'GET':
        try:
            result = dict()
            group_obj_id_list = NagiosHostgroups.objects.all().values_list('hostgroup_object_id', flat=True)
            for group_obj_id in group_obj_id_list:
                result[str(group_obj_id)] = host_group_services_helper(group_obj_id)

            return JsonResponse(result)
        
        except ObjectDoesNotExist:
            return JsonResponse(dict())
