from django.contrib import admin
from django.conf.urls import url,include
from . import views
urlpatterns = [
    url(r'^panel/manager/list/$', views.manager_list, name='manager_list'),
    url(r'^panel/manager/del/(?P<pk>\d+)/$', views.manager_del, name='manager_del'),
]
