from django.contrib import admin
from django.conf.urls import url,include
from . import views

urlpatterns = [
url('^panel/category/list/$',views.cat_list,name='cat_list'),
url('^panel/category/add/$',views.cat_add,name='cat_add'),
]
