from django.contrib import admin
from django.conf.urls import url,include
from . import views
urlpatterns = [
    url('^$',views.home,name='home'),
    url('^about/$',views.about,name='about'),
    url('^panel/$',views.panel,name='panel'),
    url('^login/$',views.mylogin,name='mylogin'),
    url('^logout/$',views.mylogout,name='mylogout'),
    url(r'^panel/setting/$', views.site_setting, name='site_setting'),
    url(r'^panel/about/setting/$', views.about_setting, name='about_setting'),
    url(r'^contact/$', views.contact, name='contact'),
    url(r'^panel/change/pass/$', views.change_pass, name='change_pass'),
    url('^register/(?P<email>.*)/(?P<pk>\d+)/$', views.myregister, name='myregister'),
    url(r'^show/data/$', views.show_data, name='show_data'),
]
