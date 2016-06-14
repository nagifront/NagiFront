from django.conf.urls import url

from . import views

urlpatterns = [ 
        url(r'^$', views.index, name='index'),
        url(r'^search$', views.search, name='search'),
        url(r'^login$', views.login, name='login'),
        url(r'^logout$', views.logout, name='logout'),
        
        url(r'^hosts/overall$', views.hosts_overall, name='hosts-overall'),
        url(r'^hosts/services$', views.hosts_services, name='hosts-services'),
        url(r'^hosts/services/configurations$', views.hosts_services_configurations, name='hosts-services-configurations'),
        url(r'^hosts/status$', views.hosts_status, name='hosts-status'),
        url(r'^hosts/comments$', views.hosts_comments, name='hosts-comments'),
        url(r'^hosts/configurations$', views.hosts_configurations, name='hosts-configurations'),
        url(r'^hosts/state-change$', views.hosts_state_change, name='hosts-state-change'),
        url(r'^hosts/parent-information$', views.hosts_parent_information, name='hosts-parent-information'),
        url(r'^hosts/ids$', views.host_id_set, name='hosts-ids'),

        url(r'^hosts/groups$', views.hosts_groups, name='hosts-groups'),
        url(r'^hosts/groups/configurations$', views.hosts_groups_configurations, name='hosts-groups-configurations'),
        url(r'^hosts/groups/hosts-state$', views.hosts_groups_hosts_state, name='hosts-groups-hosts-state'),
        url(r'^hosts/groups/service-number-by-state$', views.hosts_groups_service_number_by_state, name='host-groups-service-number-by-state'),
        url(r'^hosts/groups/trouble-trend$', views.hosts_groups_trouble_trend, name='host-groups-trouble-trend'),
        url(r'^hosts/groups/trouble-hosts$', views.hosts_groups_trouble_hosts, name='host-groups-trouble-hosts'),
        url(r'^hosts/groups/check-schedules$', views.hosts_groups_check_schedules, name='host-groups-check-schedules'),
        url(r'^hosts/groups/ids$', views.host_group_id_set, name='hosts-groups-ids'),
        
        url(r'^hosts/(?P<host_id>[0-9]+)/trend$', views.hosts_id_trend, name='hosts-id-trend'),
        
        url(r'^configuration/scheduled-downtime$', views.configuration_scheduled_downtime, name='configuration-scheduled-downtime'),
        url(r'^configuration/comments$', views.configuration_comments, name='configuration-comments'),
        url(r'^configuration/contacts$', views.configuration_contacts, name='configuration-contacts'),
        url(r'^configuration/contactgroups$', views.configuration_contactgroups, name='configuration-contactgroups'),
        url(r'^configuration/timeperiods$', views.configuration_timeperiods, name='configuration-timeperiods'),
        url(r'^configuration/commands$', views.configuration_commands, name='configuration-commands'),
        ]
