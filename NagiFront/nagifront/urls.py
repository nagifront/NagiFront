from django.conf.urls import url

from . import views

urlpatterns = [ 
        url(r'^$', views.index, name='index'),
        url(r'^login$', views.login, name='login'),
        url(r'^hosts/overall$', views.hosts_overall, name='hosts-overall'),
        url(r'^hosts/groups$', views.hosts_groups, name='hosts-groups'),
        ]
