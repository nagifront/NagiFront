from django.conf.urls import url

from . import views

urlpatterns = [ 
        url(r'^$', views.index, name='index'),
        url(r'^dashboard_setting/(?P<user_id>[0-9]+)/$', views.show_dashboard_setting, name='dashboard_setting'), 
        ]
