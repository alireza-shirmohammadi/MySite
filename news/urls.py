from django.contrib import admin
from django.conf.urls import url,include
from . import views

urlpatterns = [
    url('^news/(?P<pk>\d+)/$',views.news_detail,name='news_detail'),
    url('^panel/news/list/$',views.news_list,name='news_list'),
    url('^panel/news/add/$',views.news_add,name='news_add'),
    url('^panel/news/delete/(?P<pk>\d+)/$',views.news_delete,name='news_delete'),
    url('^panel/news/edit/(?P<pk>\d+)/$',views.news_edit,name='news_edit'),
    url(r'^panel/news/publish/(?P<pk>\d+)/$', views.news_publish, name='news_publish'),
    url(r'^panel/news/unpublish/(?P<pk>\d+)/$', views.news_unpublish, name='news_unpublish'),
    url(r'^export/news/csv/$', views.export_news_csv, name='export_news_csv'),
    url(r'^import/news/csv/$', views.import_news_csv, name='import_news_csv'),
    url('^all/news/(?P<word>.*)/$',views.news_all_show,name='news_all_show'),

]
