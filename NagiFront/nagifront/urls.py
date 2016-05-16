from django.conf.urls import url

from . import views

urlpatterns = [ 
        url(r'^$', views.index, name='index'),
        url(r'^login$', views.login, name='login'),
        url(r'^logout$', views.logout, name='logout'),
        
        url(r'^hosts/overall$', views.hosts_overall, name='hosts-overall'),
        url(r'^hosts/status$', views.hosts_status, name='hosts-status'),

        url(r'^hosts/groups$', views.hosts_groups, name='hosts-groups'),
        url(r'^hosts/groups/hosts-state$', views.hosts_groups_hosts_state, name='hosts-groups-hosts-state'),
        url(r'^hosts/groups/service-number-by-state$', views.hosts_groups_service_number_by_state, name='host-groups-service-number-by-state'),
        
        url(r'^hosts/(?P<host_id>[0-9]+)/trend$', views.hosts_id_trend, name='hosts-id-trend'),

        ]
