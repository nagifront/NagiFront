import os
import json
from datetime import datetime, timedelta, time

from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, Http404
from django.utils import timezone;

from django.conf import settings

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as django_login, logout as django_logout

from django.core.exceptions import ObjectDoesNotExist

from .customfields import CustomJSONEncoder

from django.db.models import Count
from .models import UserProfile
from .nagios_models import *

from nagifront.config_model.NagiosConfig import *

# Create your views here.

@login_required
def index(request):
    return render(request, 'nagifront/dashboard.html', {
    })

@login_required
def search(request) :
    if request.method == 'GET':
        host_id = request.GET.get('id')
        search_type = request.GET.get('type')
        if search_type == "hostGroup":
            return render(request, 'nagifront/searchHostGroup.html', {'id' : host_id})
        elif search_type == "host":
            return render(request, 'nagifront/searchHost.html', {'id' : host_id})

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
def system(request):
    host_id = request.GET.get('id')
    if host_id is not None:
        return render(request, 'nagifront/system.html', {'id' : host_id})
    else:
        return render(request, 'nagifront/system.html', {
    })

@login_required
def hosts(request):
    return render(request, 'nagifront/hosts.html', {
    })


@login_required
def setting(request):
    return render(request, 'nagifront/setting.html', {
    })

@login_required
def add_config(request, objecttype):
    message = request.session.get('message', None)
    request.session['message'] = None
    if objecttype == 'host':
        config_module = NagiosHostConfig()
    elif objecttype == 'service':
        config_module = NagiosServiceConfig()
    elif objecttype == 'hostgroup':
        config_module = NagiosHostgroupConfig()
    else:
        return Http404("No object type")
    config_module.read('you can\'t read')
    if request.method == 'POST':
        for directive in config_module.directives_list:
            val = ','.join(request.POST.getlist(directive['name']))
            config_module.edit(directive['name'], val)
        # edit
        tempfile = os.path.join(settings.NAGIOS_TEMP_FILE_DIRECTORY, config_module.gen_filename())
        filename = os.path.join(settings.NAGIOS_CONFIG_ROOT, config_module.gen_filename())
        config_module.write(tempfile)
        if not config_module.move(tempfile, filename):
            request.session['message'] = '설정 변경에 실패했습니다. 데이터를 다시 확인 해주세요'
            return redirect('add-config', objecttype=objecttype)
        # file generate
        if config_module.valid():
        # valid check
            if config_module.restart():
        # restart
                request.session['message'] = '설정이 반영되었습니다'
                return redirect('system')
            else:
                # restore
                # restart
                request.session['message'] = '설정 변경에 실패했습니다. 데이터를 다시 확인 해주세요'
                return redirect('add-config', objecttype=objecttype)
        else:
            request.session['message'] = '설정 변경에 실패했습니다. 데이터를 다시 확인 해주세요'
            return redirect('add-config', objecttype=objecttype)

    hosts = [''] + list(NagiosObjects.objects.filter(objecttype_id=1, is_active=1).values_list('name1', flat=True))
    hostgroups = [''] + list(NagiosObjects.objects.filter(objecttype_id=3, is_active=1).values_list('name1', flat=True))
    services = NagiosObjects.objects.filter(objecttype_id=2, is_active=1).values_list('name2', 'name1')
    timeperiods = NagiosObjects.objects.filter(objecttype_id=9, is_active=1).values_list('name1', flat=True)
    contactgroups = [''] + list(NagiosObjects.objects.filter(objecttype_id=10, is_active=1).values_list('name1', flat=True))
    contacts = [''] + list(NagiosObjects.objects.filter(objecttype_id=11, is_active=1).values_list('name1', flat=True))
    return render(request, 'nagifront/add-config.html', {
        'hosts': hosts,
        'hostgroups': hostgroups,
        'services': services,
        'timeperiods': timeperiods,
        'contactgroups': contactgroups,
        'contacts': contacts,
        'config_module': config_module,
        'objecttype': objecttype,
        'message': message,
    })
    

@login_required
def edit_config(request, object_id):
    message = request.session.get('message', None)
    request.session['message'] = None
    try:
        nagios_object = NagiosObjects.objects.get(pk=object_id)
        if not nagios_object.objecttype_id in [1, 2, 3] or nagios_object.is_active == 0:
            raise ObjectDoesNotExist
    except ObjectDoesNotExist:
        return Http404("No object for change configuration.")
    filename = nagios_object.name1 + ('_' + nagios_object.name2 if nagios_object.name2 is not None else '') + '.cfg'
    filename = os.path.join(settings.NAGIOS_CONFIG_ROOT, filename)
    if nagios_object.objecttype_id == 1:
        config_module = NagiosHostConfig()
    elif nagios_object.objecttype_id == 2:
        config_module = NagiosServiceConfig()
    elif nagios_object.objecttype_id == 3:
        config_module = NagiosHostgroupConfig()
    config_module.read(filename)
    # read
    if request.method == 'POST':
        for directive in config_module.directives_list:
            val = ','.join(request.POST.getlist(directive['name']))
            config_module.edit(directive['name'], val)
        # edit
        config_module.erase(filename)
        # file rm
        tempfile = os.path.join(settings.NAGIOS_TEMP_FILE_DIRECTORY, config_module.gen_filename())
        filename = os.path.join(settings.NAGIOS_CONFIG_ROOT, config_module.gen_filename())
        config_module.write(tempfile)
        config_module.move(tempfile, filename)
        # file generate
        if config_module.valid():
        # valid check
            if config_module.restart():
        # restart
                request.session['message'] = '설정이 반영되었습니다'
                return redirect('edit-config', object_id=nagios_object.object_id)
            else:
                # restore
                # restart
                request.session['message'] = '설정 변경에 실패했습니다. 데이터를 다시 확인 해주세요'
                return redirect('edit-config', object_id=nagios_object.object_id)
        else:
            request.session['message'] = '설정 변경에 실패했습니다. 데이터를 다시 확인 해주세요'
            return redirect('edit-config', object_id=nagios_object.object_id)

    hosts = [''] + list(NagiosObjects.objects.filter(objecttype_id=1, is_active=1).values_list('name1', flat=True))
    hostgroups = [''] + list(NagiosObjects.objects.filter(objecttype_id=3, is_active=1).values_list('name1', flat=True))
    services = NagiosObjects.objects.filter(objecttype_id=2, is_active=1).values_list('name2', 'name1')
    timeperiods = NagiosObjects.objects.filter(objecttype_id=9, is_active=1).values_list('name1', flat=True)
    contactgroups = [''] + list(NagiosObjects.objects.filter(objecttype_id=10, is_active=1).values_list('name1', flat=True))
    contacts = [''] + list(NagiosObjects.objects.filter(objecttype_id=11, is_active=1).values_list('name1', flat=True))
    return render(request, 'nagifront/edit-config.html', {
        'hosts': hosts,
        'hostgroups': hostgroups,
        'services': services,
        'timeperiods': timeperiods,
        'contactgroups': contactgroups,
        'contacts': contacts,
        'object': nagios_object,
        'config_module': config_module,
        'message': message,
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
            host = NagiosHosts.objects.get(host_object_id = host_id)
            history = list(NagiosHostchecks.objects.filter(host_object_id=host_id).values('state', 'is_raw_check', 'end_time').order_by('-end_time'))

            for i in range(len(history) - 2, -1, -1):
                if history[i]['state'] == history[i+1]['state']:
                    del history[i];

            return JsonResponse({'trends':history, 'host':host}, encoder=CustomJSONEncoder)
    
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
                host_alias = NagiosHosts.objects.get(host_object_id=host_id).alias
                host_status.alias = host_alias
                result['hosts'] = [ host_status ]
                return JsonResponse(result, encoder=CustomJSONEncoder)
            else:
                host_statuses = list(NagiosHoststatus.objects.all())
                host_alias_data = NagiosHosts.objects.values('host_object_id', 'alias')
                
                host_alias_map = {}
                for host_alias in host_alias_data:
                    host_alias_map[host_alias['host_object_id']] = host_alias['alias']

                for status in host_statuses:
                    status.alias = host_alias_map[status.host_object_id]

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
            hosts_statuses = NagiosHoststatus.objects.all().values('host_object_id', 'current_state', 'last_state_change', 'output', 'is_flapping')  \
                                                           .order_by('host_object_id')
            hosts = NagiosHosts.objects.all().values('host_object_id', 'alias')
            result = {'hosts':[]}

            for host in hosts:
                host_status = hosts_statuses.get(host_object_id=host['host_object_id'])
                result['hosts'].append({
                                'alias': host['alias'],
                                'output': host_status['output'],
                                'is_flapping': host_status['is_flapping'],
                                'state': host_status['current_state'],
                                'last_state_change': host_status['last_state_change']
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
                group_service_states = NagiosServicestatus.objects.filter(service_object_id__in=group_services.values_list('service_object_id')) \
                                                                  .exclude(current_state=0)                                                      \
                                                                  .values('service_object_id',
                                                                          'current_state',
                                                                          'last_state_change',
                                                                          'output',
                                                                          'is_flapping')          \
                                                                  .order_by('-last_state_change')
                
                host_alias_map = NagiosHosts.objects.filter(host_object_id__in=group_members)   \
                                                    .values('host_object_id', 'alias')

                result = {"trouble_hosts":[]}
                for service in group_service_states:
                    service_data = {}
                    service_data['state'] = service['current_state']
                    service_data['time'] = service['last_state_change']
                    service_data['output'] = service['output']
                    service_data['is_flapping'] = service['is_flapping']
                        
                    service_map = group_services.get(service_object_id=service['service_object_id'])

                    service_data['service_name'] = service_map['display_name']
                    service_data['host_name'] = host_alias_map.get(host_object_id=service_map['host_object_id'])['alias']
                    result['trouble_hosts'].append(service_data)

                return JsonResponse(result, json_dumps_params={'ensure_ascii':False})

            else:
                hosts = NagiosHosts.objects.values('host_object_id', 'alias')
                services = NagiosServices.objects.values('service_object_id', 'host_object_id', 'display_name')

                trouble_services = NagiosServicestatus.objects.exclude(current_state=0)                                                                     \
                                                              .values('service_object_id',
                                                                      'current_state',
                                                                      'last_state_change',
                                                                      'output',
                                                                      'is_flapping')          \
                                                              .order_by('-last_state_change')
                
                result = {"trouble_hosts":[]}
                for service in trouble_services:
                    service_data = {}
                    service_data['state'] = service['current_state']
                    service_data['time'] = service['last_state_change']
                    service_data['output'] = service['output']
                    service_data['is_flapping'] = service['is_flapping']
                        
                    service_map = services.get(service_object_id=service['service_object_id'])

                    service_data['service_name'] = service_map['display_name']
                    service_data['host_name'] = hosts.get(host_object_id=service_map['host_object_id'])['alias']
                    result['trouble_hosts'].append(service_data)
                
                return JsonResponse(result, json_dumps_params={'ensure_ascii':False})

        except ObjectDoesNotExist:
            return JsonResponse(dict())
    else:
        return JsonResponse(dict())

@login_required
def hosts_groups_check_schedules(request):
    if request.method == 'GET':
        try:
            group_obj_id = request.GET.get('host_group_id')

            if group_obj_id is not None:
                group_id = NagiosHostgroups.objects.get(hostgroup_object_id=group_obj_id).hostgroup_id
                group_members = NagiosHostgroupMembers.objects.filter(hostgroup_id=group_id)                    \
                                                              .values_list('host_object_id', flat=True)
                group_services = NagiosServices.objects.filter(host_object_id__in=group_members)                        \
                                                       .values('service_object_id', 'host_object_id', 'display_name')
                group_service_schedules = NagiosServicestatus.objects.filter(service_object_id__in=group_services.values_list('service_object_id'))    \
                                                                  .values('service_object_id', 'last_check', 'next_check')                             \
                                                                  .order_by('next_check')
                host_alias_map = NagiosHosts.objects.filter(host_object_id__in=group_members)   \
                                                    .values('host_object_id', 'alias')

                result = {'check_schedules':[]}
                for service in group_service_schedules:
                    service_schedule = {}
                    service_schedule['next_check_time'] = service['next_check']
                    service_schedule['last_check_time'] = service['last_check']

                    service_map = group_services.get(service_object_id=service['service_object_id'])

                    service_schedule['service_name'] = service_map['display_name']
                    service_schedule['host_name'] = host_alias_map.get(host_object_id=service_map['host_object_id'])['alias']

                    result['check_schedules'].append(service_schedule)

                return JsonResponse(result, json_dumps_params={'ensure_ascii':False})
            else:
                hosts = NagiosHosts.objects.values('host_object_id', 'alias')
                services = NagiosServices.objects.values('service_object_id', 'host_object_id', 'display_name')

                service_schedules = NagiosServicestatus.objects.values('service_object_id', 'last_check', 'next_check')    \
                                                               .order_by('next_check')
                result = {"check_schedules":[]}
                for service in service_schedules:
                    service_schedule = {}
                    service_schedule['next_check_time'] = service['next_check']
                    service_schedule['last_check_time'] = service['last_check']

                    service_map = services.get(service_object_id=service['service_object_id'])

                    service_schedule['service_name'] = service_map['display_name']
                    service_schedule['host_name'] = hosts.get(host_object_id=service_map['host_object_id'])['alias']

                    result['check_schedules'].append(service_schedule)

                return JsonResponse(result, json_dumps_params={'ensure_ascii':False})
        except ObjectDoesNotExist:
            return JsonResponse(dict())
    else:
        return JsonResponse(dict())

@login_required
def hosts_parent_information(request):
    if request.method == 'GET':
        try:
            hosts = NagiosHosts.objects.values('host_id', 'host_object_id', 'alias')
            host_parent_data = NagiosHostParenthosts.objects.values('host_id', 'parent_host_object_id')

            result = {'host_dependency':[]}
            for host in hosts:
                host_data = {}
                host_data['alias'] = host['alias']
                host_data['host_object_id'] = host['host_object_id']
                
                try:
                    host_parent = host_parent_data.get(host_id=host['host_id'])['parent_host_object_id']
                except NagiosHostParenthosts.DoesNotExist:
                    host_parent = None
                finally:
                    host_data['parent_host_object_id'] = host_parent

                result['host_dependency'].append(host_data)

            return JsonResponse(result)
        except ObjectDoesNotExist:
            return JsonResponse(dict())
    else:
        return JsonResponse(dict())

@login_required
def configuration_scheduled_downtime(request):
    if request.method == 'GET':
        try:
            downtime_list = NagiosScheduleddowntime.objects.filter(downtime_type=2)         \
                                                           .values('object_id',             
                                                                   'entry_time',            
                                                                   'comment_data',          
                                                                   'scheduled_start_time', 
                                                                   'scheduled_end_time')    \
                                                           .order_by('scheduled_start_time')
            host_alias_map = {}
            host_data_list = NagiosHosts.objects.values('host_object_id','alias')
            for host in host_data_list:
                host_alias_map[host['host_object_id']] = host['alias']

            result = {'scheduled_downtime':[]}
            for downtime_entry in downtime_list:
                entry_data = {}
                entry_data['entry_time'] = downtime_entry['entry_time']
                entry_data['comment_data'] = downtime_entry['comment_data']
                entry_data['scheduled_start_time'] = downtime_entry['scheduled_start_time']
                entry_data['scheduled_end_time'] = downtime_entry['scheduled_end_time']
                entry_data['host_name'] = host_alias_map[downtime_entry['object_id']]
                result['scheduled_downtime'].append(entry_data)

            return JsonResponse(result)
        except ObjectDoesNotExist:
            return JsonResponse(dict())
    else:
        return JsonResponse(dict())

@login_required
def configuration_comments(request):
    if request.method == 'GET':
        try:
            comments_list = NagiosComments.objects.values('object_id',
                                                          'comment_type',
                                                          'comment_time',            
                                                          'comment_data',          
                                                          'author_name')    \
                                                  .order_by('-comment_time')
            host_alias_map = {}
            host_data_list = NagiosHosts.objects.values('host_object_id','alias')
            for host in host_data_list:
                host_alias_map[host['host_object_id']] = host['alias']

            service_alias_map = {}
            service_data_list = NagiosServices.objects.values('service_object_id', 'host_object_id', 'display_name')
            for service in service_data_list:
                service_alias_map[service['service_object_id']] = {
                                                                    'host_object_id': service['host_object_id'],
                                                                    'host_alias': host_alias_map[service['host_object_id']],
                                                                    'display_name': service['display_name']
                                                                  }

            result = {'comments':[]}
            for comment_entry in comments_list:
                entry_data = {}
                entry_data['time'] = comment_entry['comment_time']
                entry_data['contents'] = comment_entry['comment_data']
                entry_data['author'] = comment_entry['author_name']
                if comment_entry['comment_type'] == 1:
                    entry_data['comment_type'] = 'host'
                    entry_data['host_name'] = host_alias_map[comment_entry['object_id']]
                    entry_data['service_name'] = None
                else:
                    entry_data['comment_type'] = 'service'
                    entry_data['host_name'] = (service_alias_map[comment_entry['object_id']])['host_alias']
                    entry_data['service_name'] = (service_alias_map[comment_entry['object_id']])['display_name']
                result['comments'].append(entry_data)

            return JsonResponse(result)
        except ObjectDoesNotExist:
            return JsonResponse(dict())
    else:
        return JsonResponse(dict())

@login_required
def hosts_services(request):
    if request.method == 'GET':
        try:
            host_obj_id = request.GET.get('host_id')

            if host_obj_id is not None:
                service_data_list = NagiosServices.objects.filter(host_object_id=host_obj_id)           \
                                                          .values('display_name', 'service_object_id')
                
                service_name_map = {}
                service_id_list = []
                for service_data in service_data_list:
                    service_obj_id = service_data['service_object_id']
                    service_name_map[service_obj_id] = service_data['display_name']
                    service_id_list.append(service_obj_id)
                
                service_status_list = NagiosServicestatus.objects.filter(service_object_id__in=service_id_list)

                result = {'services':[]}
                state_num = [0, 0, 0, 0]
                for service_entry in service_status_list:
                    service_entry.display_name = service_name_map[service_entry.service_object_id]
                    state_num[service_entry.current_state] += 1
                    result['services'].append(service_entry)
                
                result['state_number']={'Ok':state_num[0], 'Warning':state_num[1], 'Critical':state_num[2], 'Unknown':state_num[3]}
                return JsonResponse(result, encoder=CustomJSONEncoder)
                                                                           
            else: # For now, NagiFront doesn't provide a service status API for all services. This API should be host-specific.
                return JsonResponse(dict()) 
        except ObjectDoesNotExist:
            return JsonResponse(dict())
    else:
        return JsonResponse(dict())

@login_required
def host_id_set(request):
    if request.method == 'GET':
        try:
            result = {'ids':[]}
            host_list = NagiosHosts.objects.values('host_object_id', 'alias')
            for host in host_list:
                m = {}
                m['name'] = host['alias']
                m['host_object_id'] = host['host_object_id']
                result['ids'].append(m)

            return JsonResponse(result)
        except ObjectDoesNotExist:
            return JsonResponse(dict())
    else:
        return JsonResponse(dict())

@login_required
def host_group_id_set(request):
    if request.method == 'GET':
        try:
            result = {'ids':[]}
            hostgroup_list = NagiosHostgroups.objects.values('hostgroup_object_id', 'alias')
            for hostgroup in hostgroup_list:
                m = {}
                m['name']  = hostgroup['alias']
                m['hostgroup_object_id'] = hostgroup['hostgroup_object_id']
                result['ids'].append(m)

            return JsonResponse(result)
        except ObjectDoesNotExist:
            return JsonResponse(dict())
    else:
        return JsonResponse(dict())

@login_required
def hosts_comments(request):
    if request.method == 'GET':
        try:
            host_obj_id = request.GET.get('host_id')
            if host_obj_id is not None:
                comment_list = NagiosComments.objects.values('comment_time', 'author_name', 'comment_data') \
                                                     .filter(object_id=host_obj_id)
                comment_list = list(comment_list)
                host_name = NagiosHosts.objects.get(host_object_id=host_obj_id).alias

                for comment in comment_list:
                    comment['host_name'] = host_name
                    # Rename dictionary keys properly
                    comment['contents'] = comment.pop('comment_data')
                    comment['author'] = comment.pop('author_name')
                    comment['time'] = comment.pop('comment_time')
                
                result = {'comments':comment_list}
                return JsonResponse(result)
            else:
                comment_list = NagiosComments.objects.values('comment_time', 'author_name', 'comment_data', 'object_id') \
                                                     .filter(comment_type=1) # Filter host comments only
                
                comment_list = list(comment_list)
                host_name_list = NagiosHosts.objects.values('host_object_id', 'alias')
                host_name_map = {}
                for host_data in host_name_list:
                    host_name_map[host_data['host_object_id']] = host_data['alias']

                for comment in comment_list:
                    comment['host_name'] = host_name_map['object_id']
                    # Rename dictionary keys properly
                    comment['contents'] = comment.pop('comment_data')
                    comment['author'] = comment.pop('author_name')
                    comment['time'] = comment.pop('comment_time')
                    # Remove object id
                    comment.pop('object_id')

                result = {'comments':comment_list}
                return JsonResponse(result)
        except ObjectDoesNotExist:
            return JsonResponse(dict())
    else:
        return JsonResponse(dict())

@login_required
def hosts_configurations(request):
    if request.method == 'GET':
        try:
            host_configs = list(NagiosHosts.objects.values())
            host_name_map = {}
            for host in host_configs:
                host_name_map[host['host_object_id']] = host['alias']

            host_parent_list = NagiosHostParenthosts.objects.values('host_id', 'parent_host_object_id')
            host_parent_map = {}
            for hp in host_parent_list:
                host_parent_map[hp['host_id']] = host_name_map[hp['parent_host_object_id']]

            timeperiod_list = NagiosTimeperiods.objects.values('alias', 'timeperiod_object_id')
            timeperiod_name_map = {}
            for tp in timeperiod_list:
                timeperiod_name_map[tp['timeperiod_object_id']] = tp['alias']

            contactgroup_list = NagiosHostContactgroups.objects.values('host_id', 'contactgroup_object_id')
            contactgroup_name_list = NagiosContactgroups.objects.values('contactgroup_object_id', 'alias')
            
            contactgroup_name_map = {}
            for cg in contactgroup_name_list:
                contactgroup_name_map[cg['contactgroup_object_id']] = cg['alias']
            
            host_contactgroup_map = {}
            for hcg in contactgroup_list:
                host_contactgroup_map[hcg['host_id']] = contactgroup_name_map[hcg['contactgroup_object_id']]
            
            for host in host_configs:
                host['check_period'] = timeperiod_name_map.get(host['check_timeperiod_object_id'], None)
                host['notification_period'] = timeperiod_name_map.get(host['notification_timeperiod_object_id'], None)
                host['contact_group'] = host_contactgroup_map[host['host_id']]
                host['parent_host'] = host_parent_map.get(host['host_id'], None)

            result = {'host_configurations':host_configs}
            return JsonResponse(result)
            
        except ObjectDoesNotExist:
            return JsonResponse(dict())
    else:
        return JsonResponse(dict())

@login_required
def hosts_groups_configurations(request):
    if request.method == 'GET':
        try:
            member_list = NagiosHostgroupMembers.objects.values('hostgroup_id', 'host_object_id')
            group_member_map = {}
            for member in member_list:
                if member['hostgroup_id'] in group_member_map:
                    group_member_map[member['hostgroup_id']].append(member['host_object_id'])
                else:
                    group_member_map[member['hostgroup_id']] = [member['host_object_id']]

            host_list = NagiosHosts.objects.values('host_object_id', 'alias')
            host_alias_map = {}
            for host in host_list:
                host_alias_map[host['host_object_id']] = host['alias']

            hostgroup_obj_list = NagiosObjects.objects.filter(objecttype_id=3).values('object_id', 'name1')
            hostgroup_name_map = {}
            for group in hostgroup_obj_list:
                hostgroup_name_map[group['object_id']] = group['name1']

            group_list = list(NagiosHostgroups.objects.values())
            for group in group_list:
                group['host_members'] = [host_alias_map[m_id] for m_id in group_member_map[group['hostgroup_id']]]
                group['group_name'] = hostgroup_name_map[group['hostgroup_object_id']]
                group['description'] = group.pop('alias') # Renaming the key 'alias' to 'description'

            result = {'hostgroups':group_list}
            return JsonResponse(result)
        except ObjectDoesNotExist:
            return JsonResponse(dict())
    else:
        return JsonResponse(dict())

@login_required
def hosts_services_configurations(request):
    if request.method == 'GET':
        try:
            host_name_list = NagiosHosts.objects.values('host_object_id', 'alias')
            host_name_map = {}
            for host in host_name_list:
                host_name_map[host['host_object_id']] = host['alias']

            timeperiod_list = NagiosTimeperiods.objects.values('alias', 'timeperiod_object_id')
            timeperiod_name_map = {}
            for tp in timeperiod_list:
                timeperiod_name_map[tp['timeperiod_object_id']] = tp['alias']

            contactgroup_list = NagiosServiceContactgroups.objects.values('service_id', 'contactgroup_object_id')
            contactgroup_name_list = NagiosContactgroups.objects.values('contactgroup_object_id', 'alias')
            
            contactgroup_name_map = {}
            for cg in contactgroup_name_list:
                contactgroup_name_map[cg['contactgroup_object_id']] = cg['alias']
            
            service_contactgroup_map = {}
            for scg in contactgroup_list:
                service_contactgroup_map[scg['service_id']] = contactgroup_name_map[scg['contactgroup_object_id']]
            
            command_list =  NagiosObjects.objects.filter(objecttype_id=12).values('object_id', 'name1')
            command_name_map = {}
            for cmd in command_list:
                command_name_map[cmd['object_id']] = cmd['name1']

            service_list = list(NagiosServices.objects.values())
            for service in service_list:
                service['host'] = host_name_map[service['host_object_id']]
                if service['check_command_args'] == "":
                    service['check_command'] = command_name_map[service['check_command_object_id']]
                else:
                    service['check_command'] = command_name_map[service['check_command_object_id']] + "!" + service['check_command_args']
               
                service['check_period'] = timeperiod_name_map.get(service['check_timeperiod_object_id'], None)
                service['notification_period'] = timeperiod_name_map.get(service['notification_timeperiod_object_id'], None)
                service['contact_group'] = service_contactgroup_map[service['service_id']]

            result = {'services':service_list}
            return JsonResponse(result)
        except ObjectDoesNotExist:
            return JsonResponse(dict())
    else:
        return JsonResponse(dict())

@login_required
def configuration_contacts(request):
    if request.method == 'GET':
        try:
            timeperiod_list = NagiosTimeperiods.objects.values('alias', 'timeperiod_object_id')
            timeperiod_name_map = {}
            for tp in timeperiod_list:
                timeperiod_name_map[tp['timeperiod_object_id']] = tp['alias']

            contact_obj_list =  NagiosObjects.objects.filter(objecttype_id=10).values('object_id', 'name1')
            contact_name_map = {}
            for cnt in contact_obj_list:
                contact_name_map[cnt['object_id']] = cnt['name1']
            
            contact_list = list(NagiosContacts.objects.values())
            for contact in contact_list:
                contact['contact_name'] = contact_name_map[contact['contact_object_id']]
                contact['service_notification_period'] = timeperiod_name_map[contact['service_timeperiod_object_id']]
                contact['host_notification_period'] = timeperiod_name_map[contact['host_timeperiod_object_id']]
                contact['description'] = contact.pop('alias')

            result = {'contacts':contact_list}
            return JsonResponse(result)
        
        except ObjectDoesNotExist:
            return JsonResponse(dict())
    else:
        return JsonResponse(dict())

@login_required
def configuration_contactgroups(request):
    if request.method == 'GET':
        try:
            contact_obj_list =  NagiosObjects.objects.filter(objecttype_id=10).values('object_id', 'name1')
            contact_name_map = {}
            for cnt in contact_obj_list:
                contact_name_map[cnt['object_id']] = cnt['name1']
            
            contact_member_list = NagiosContactgroupMembers.objects.values('contactgroup_id', 'contact_object_id')
            contact_member_map = {}
            for cm in contact_member_list:
                if cm['contactgroup_id'] in contact_member_map:
                    contact_member_map[cm['contactgroup_id']].append(contact_name_map[cm['contact_object_id']])
                else:
                    contact_member_map[cm['contactgroup_id']] = [contact_name_map[cm['contact_object_id']]]

            contactgroup_obj_list = NagiosObjects.objects.filter(objecttype_id=11).values('object_id', 'name1')
            contactgroup_name_map = {}
            for cg in contactgroup_obj_list:
                contactgroup_name_map[cg['object_id']] = cg['name1']

            contactgroup_list = list(NagiosContactgroups.objects.values())
            for cg in contactgroup_list:
                cg['members'] = contact_member_map[cg['contactgroup_id']]
                cg['contactgroup_name'] = contactgroup_name_map[cg['contactgroup_object_id']]
                cg['description'] = cg.pop('alias')

            result = {'contactgroups':contactgroup_list}
            return JsonResponse(result)
        except ObjectDoesNotExist:
            return JsonResponse(dict())
    else:
        return JsonResponse(dict())

@login_required
def configuration_timeperiods(request):
    if request.method == 'GET':
        try:
            timerange_list = NagiosTimeperiodTimeranges.objects.values()
            timeperiod_range_map = {}
            for tr in timerange_list:
                if tr['timeperiod_id'] in timeperiod_range_map:
                    timeperiod_range_map[tr['timeperiod_id']].append({'day':tr['day'], 'start_sec':tr['start_sec'], 'end_sec':tr['end_sec']})
                else:
                    timeperiod_range_map[tr['timeperiod_id']] = [{'day':tr['day'], 'start_sec':tr['start_sec'], 'end_sec':tr['end_sec']}]

            timeperiod_obj_list = NagiosObjects.objects.filter(objecttype_id=9).values('object_id', 'name1')
            timeperiod_name_map = {}
            for tp in timeperiod_obj_list:
                timeperiod_name_map[tp['object_id']] = tp['name1']
            
            timeperiod_list = list(NagiosTimeperiods.objects.values())
            for timeperiod in timeperiod_list:
                timeperiod['time_ranges'] = timeperiod_range_map.get(timeperiod['timeperiod_id'], None)
                timeperiod['timeperiod_name'] = timeperiod_name_map[timeperiod['timeperiod_object_id']]
                timeperiod['description'] = timeperiod.pop('alias')

            result = {'timeperiods':timeperiod_list}
            return JsonResponse(result)

        except ObjectDoesNotExist:
            return JsonResponse(dict())
    else:
        return JsonResponse(dict())

@login_required
def configuration_commands(request):
    if request.method == 'GET':
        try:
            command_obj_list = NagiosObjects.objects.filter(objecttype_id=12).values('object_id', 'name1')
            command_name_map = {}
            for cmd in command_obj_list:
                command_name_map[cmd['object_id']] = cmd['name1']

            command_list = list(NagiosCommands.objects.values())
            for command in command_list:
                command['command_name'] = command_name_map[command['object_id']]

            result = {'commands':command_list}
            return JsonResponse(result)
        except ObjectDoesNotExist:
            return JsonResponse(dict())
    else:
        return JsonResponse(dict())

@login_required
def service_id_trend(request, service_id):
    if request.method == 'GET':
        try:
            service = NagiosServices.objects.get(service_object_id = service_id)
            history = list(NagiosServicechecks.objects.filter(service_object_id=service_id).values('state', 'end_time').order_by('-end_time'))

            for i in range(len(history) - 2, -1, -1):
                if history[i]['state'] == history[i+1]['state']:
                    del history[i];

            return JsonResponse({'trends':history, 'service':service}, encoder=CustomJSONEncoder)
        except ObjectDoesNotExist:
            return JsonResponse(dict())
    else:
        return JsonResponse(dict())

""" GET API Template
@login_required
def some_api_name(request):
    if request.method == 'GET':
        try:
            # DO
            # SOMTHING
            # NEEDED
        except ObjectDoesNotExist:
            return JsonResponse(dict())
    else:
        return JsonResponse(dict())
"""
