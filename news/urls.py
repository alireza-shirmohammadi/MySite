from django.contrib import admin
from django.conf.urls import url,include
from . import views

urlpatterns = [
    url('^news/(?P<pk>\d+)/$',views.news_detail,name='news_detail'),
    url('^panel/news/list/$',views.news_list,name='news_list'),
    url('^panel/news/add/$',views.news_add,name='news_add'),
    url('^panel/news/delete/(?P<pk>\d+)/$',views.news_delete,name='news_delete'),
    url('^panel/news/edit/(?P<pk>\d+)/$',views.news_edit,name='news_edit'),

]
