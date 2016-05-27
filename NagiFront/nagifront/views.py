import json
from datetime import datetime, timedelta, time

from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.utils import timezone;

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as django_login

from django.core.exceptions import ObjectDoesNotExist

from .customfields import CustomJSONEncoder

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

def logout(request):
    django_logout(request)
    return redirect('login')

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
        services_state_count = list(NagiosServicestatus.objects.filter(service_object_id__in=services)  \
                                                               .values('current_state')                 \
                                                               .annotate(Count('current_state'))        \
                                                               .order_by('current_state')               \
                                                               .values_list('current_state', 'current_state__count'))
        # Handling cases which certain state is not existed
        # ex) 'Ok':4, 'Warning':0, 'Critical':3, 'Unknown':1 -> before this loop, services_state_count = [(0,4), (2,3), (3,1)]
        services_state_count += [(5,0), (6,0), (7,0), (8,0)]
        for i in range(4):
            if services_state_count[i][0] != i:
                services_state_count.insert(i, (0,0))
        
        return {
            'alias':alias, 
            'ok':services_state_count[0][1], 
            'warning':services_state_count[1][1], 
            'critical':services_state_count[2][1], 
            'unknown':services_state_count[3][1]
        }

    if request.method == 'GET':
        try:
            result = dict()
            group_obj_id_list = NagiosHostgroups.objects.all().values_list('hostgroup_object_id', flat=True)
            for group_obj_id in group_obj_id_list:
                result[str(group_obj_id)] = host_group_services_helper(group_obj_id)

            return JsonResponse(result)
        
        except ObjectDoesNotExist:
            return JsonResponse(dict())

@login_required
def hosts_id_trend(request, host_id):
    try:
        if request.method == 'GET':
            history = list(NagiosHostchecks.objects.filter(host_object_id=host_id).values('state', 'is_raw_check', 'end_time').order_by('-end_time'))

            for i in range(len(history) - 2, -1, -1):
                if history[i]['state'] == history[i+1]['state']:
                    del history[i];

            return JsonResponse({'trends':history}, safe=False)
    
    except ObjectDoesNotExist:
        return JsonResponse(dict())

@login_required
def hosts_status(request):
    try:
        if request.method == 'GET':
            result = dict()
            host_id = request.GET.get('host_id')
            if host_id is not None:
                host_status = NagiosHoststatus.objects.get(host_object_id=host_id)
                result['hosts'] = [ host_status ]
                return JsonResponse(result, encoder=CustomJSONEncoder)
            else:
                host_statuses = list(NagiosHoststatus.objects.all())
                result['hosts'] = host_statuses
                return JsonResponse(result, encoder=CustomJSONEncoder)
   
    except ObjectDoesNotExist:
       return JsonResponse(dict())

@login_required
def hosts_groups_hosts_state(request):
    if request.method == 'GET':
        try:
            result = dict()
            group_obj_id = request.GET.get('host_group_id')

            if group_obj_id is not None:            
                group = NagiosHostgroups.objects.get(hostgroup_object_id=group_obj_id)
                alias = group.alias
                host_list = NagiosHostgroupMembers.objects.filter(hostgroup_id=group.hostgroup_id).values_list('host_object_id', flat=True)
                status_list = list(NagiosHoststatus.objects.filter(host_object_id__in=host_list)        \
                                                           .values('current_state')                     \
                                                           .annotate(Count('current_state'))            \
                                                           .order_by('current_state')                   \
                                                           .values_list('current_state', 'current_state__count'))
                
                # Handling cases which certain state is not existed
                # ex) 'Up':3, 'Down':0, 'Unreachable':1 -> before this loop, status_list = [(0,3), (2,1)]
                status_list += [(5,0), (6,0), (7,0)]
                for i in range(3):
                    if status_list[i][0] != i:
                        status_list.insert(i, (0,0))

                result[str(group_obj_id)] = {'alias':alias, 'up':status_list[0][1], 'down':status_list[1][1], 'unreachable':status_list[2][1]}

            return JsonResponse(result)      
        
        except ObjectDoesNotExist:
            return JsonResponse(dict())


@login_required
def hosts_groups_trouble_trend(request):
    if request.method == 'GET':
        group_id = request.GET.get('host_group_id')
        time_scale = request.GET.get('time-scale')

        if group_id is not None and time_scale is not None:
            group_host_list = NagiosHostgroupMembers.objects\
                                                    .filter(hostgroup_id=(NagiosHostgroups.objects.get(hostgroup_object_id=group_id).hostgroup_id))\
                                                    .values_list('host_object_id', flat=True)
            group_service_list = NagiosServices.objects.filter(host_object_id__in=group_host_list).values_list('service_object_id', flat=True)
            if time_scale == 'day':
                # Get the history of recent 24 hours
                history = list(NagiosServicechecks.objects.filter(service_object_id__in=group_service_list,             \
                                                                  end_time__gte=timezone.localtime(timezone.now())-timedelta(hours=24))     \
                                                          .values('state', 'end_time')  \
                                                          .order_by('-end_time'))
                # Takes the datetime object as an argument, and returns a tuple of year,month,date,hour
                dt_tuple = lambda t: (t.year, t.month, t.day, t.hour)
                timeslot_list = [dt_tuple(timezone.localtime(timezone.now())-timedelta(hours=x)) for x in range(23, -1, -1)] # Timeslot tuple list

                grouped_history = [[sc['state'] for sc in history if (dt_tuple(sc['end_time']) == timeslot)] for timeslot in timeslot_list]
                state_history = [[l.count(0), l.count(1), l.count(2), l.count(3)] for l in grouped_history]

                result = {'time-scale': time_scale, 'time': {}}
                for i in range(len(timeslot_list)):
                    key = str(timeslot_list[i][0]) + '-'    \
                        + str(timeslot_list[i][1]) + '-'    \
                        + str(timeslot_list[i][2]) + '-'    \
                        + str(timeslot_list[i][3])          # ex) '2016-05-17-04' = 16/05/17 04:00
                    result['time'][key] = { 
                                    'ok': state_history[i][0],
                                    'warning': state_history[i][1],
                                    'critical': state_history[i][2],
                                    'unknown': state_history[i][3]
                                    }

                return JsonResponse(result)

            elif time_scale == 'week':
                # Get the history of recent 7 days
                history = NagiosServicechecks.objects.filter(service_object_id__in=group_service_list,          \
                                                             end_time__gte=timezone.localtime(timezone.now())-timedelta(days=7))    \
                                                     .values('state', 'end_time')   \
                                                     .order_by('-end_time')
                # Takes the datetime object as an argument, and returns a tuple of year,month,date
                dt_tuple = lambda t: (t.year, t.month, t.day)
                timeslot_list = [dt_tuple(timezone.localtime(timezone.now())-timedelta(days=x)) for x in range(6, -1, -1)] # Timeslot tuple list

                grouped_history = [[sc['state'] for sc in history if (dt_tuple(sc['end_time']) == timeslot)] for timeslot in timeslot_list]
                state_history = [[l.count(0), l.count(1), l.count(2), l.count(3)] for l in grouped_history]

                result = {'time-scale': time_scale, 'time': {}}
                for i in range(len(timeslot_list)):
                    key = str(timeslot_list[i][0]) + '-'    \
                        + str(timeslot_list[i][1]) + '-'    \
                        + str(timeslot_list[i][2])
                    result['time'][key] = { 
                                    'ok': state_history[i][0],
                                    'warning': state_history[i][1],
                                    'critical': state_history[i][2],
                                    'unknown': state_history[i][3]
                                    }

                return JsonResponse(result)
            else:
                return JsonResponse(dict())
        else:
            return JsonResponse(dict())
    else:
        return JsonResponse(dict())


@login_required
def hosts_state_change(request):
    if request.method == 'GET':
        try:
            hosts_statuses = NagiosHoststatus.objects.all().values('host_object_id', 'current_state', 'last_state_change')  \
                                                           .order_by('host_object_id')
            hosts = NagiosHosts.objects.all().values('host_object_id', 'alias')
            result = {'hosts':[]}

            for host in hosts:
                host_status = hosts_statuses.get(host_object_id=host['host_object_id'])
                result['hosts'].append({
                                'alias':host['alias'],
                                'state': host_status['current_state'],
                                'last_state_change':host_status['last_state_change']
                                })

            return JsonResponse(result, json_dumps_params={'ensure_ascii':False} )

        except ObjectDoesNotExist:
            return JsonResponse(dict())
    else:
        return JsonResponse(dict())

@login_required
def hosts_groups_trouble_hosts(request):
    if request.method == 'GET':
        try:
            group_obj_id = request.GET.get('host_group_id')

            if group_obj_id is not None:
                group_id = NagiosHostgroups.objects.get(hostgroup_object_id=group_obj_id).hostgroup_id
                group_members = NagiosHostgroupMembers.objects.filter(hostgroup_id=group_id)                    \
                                                              .values_list('host_object_id', flat=True)
                group_services = NagiosServices.objects.filter(host_object_id__in=group_members)                        \
                                                       .values('service_object_id', 'host_object_id', 'display_name')
                group_service_states = NagiosServicestatus.objects.filter(service_object_id__in=group_services.values_list('service_object_id'))    \
                                                                  .exclude(current_state=0)                                                         \
                                                                  .values('service_object_id', 'current_state', 'last_state_change')                \
                                                                  .order_by('-last_state_change')
                
                host_alias_map = NagiosHosts.objects.filter(host_object_id__in=group_members)   \
                                                    .values('host_object_id', 'alias')

                result = {"trouble_hosts":[]}
                for service in group_service_states:
                    service_data = {}
                    service_data['state'] = service['current_state']
                    service_data['time'] = service['last_state_change']
                        
                    service_map = group_services.get(service_object_id=service['service_object_id'])

                    service_data['service_name'] = service_map['display_name']
                    service_data['host_name'] = host_alias_map.get(host_object_id=service_map['host_object_id'])['alias']
                    result['trouble_hosts'].append(service_data)

                return JsonResponse(result, json_dumps_params={'ensure_ascii':False})

            else:
                hosts = NagiosHosts.objects.values('host_object_id', 'alias')
                services = NagiosServices.objects.values('service_object_id', 'host_object_id', 'display_name')

                trouble_services = NagiosServicestatus.objects.exclude(current_state=0)                                             \
                                                              .values('service_object_id', 'current_state', 'last_state_change')    \
                                                              .order_by('-last_state_change')
                
                result = {"trouble_hosts":[]}
                for service in trouble_services:
                    service_data = {}
                    service_data['state'] = service['current_state']
                    service_data['time'] = service['last_state_change']
                        
                    service_map = services.get(service_object_id=service['service_object_id'])

                    service_data['service_name'] = service_map['display_name']
                    service_data['host_name'] = hosts.get(host_object_id=service_map['host_object_id'])['alias']
                    result['trouble_hosts'].append(service_data)
                
                return JsonResponse(result, json_dumps_params={'ensure_ascii':False})

        except ObjectDoesNotExist:
            return JsonResponse(dict())
    else:
        return JsonResponse(dict())
