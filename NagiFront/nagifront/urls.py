from django.conf.urls import url

from . import views

urlpatterns = [ 
        url(r'^$', views.index, name='index'),
        url(r'^login$', views.login, name='login'),
        url(r'^hosts/overall$', views.hosts_overall, name='hosts-overall'),
        url(r'^hosts/groups$', views.hosts_groups, name='hosts-groups'),
        url(r'^hosts/groups/service-number-by-state$', views.hosts_groups_service_number_by_state, name='host-groups-service-number-by-state'),
        ]
