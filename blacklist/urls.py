from django.conf.urls import url
from . import views

urlpatterns = [

     url(r'^blacklist/$', views.black_list, name='black_list'),
     url(r'^blacklist/add/$', views.ip_add, name='ip_add'),
     url(r'^blacklist/del/(?P<pk>\d+)/$', views.ip_del, name='ip_del'),

]
