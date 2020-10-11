from django.contrib import admin
from django.conf.urls import url,include
from . import views

urlpatterns = [
url('^panel/subcategory/list/$',views.subcat_list,name='subcat_list'),
url('^panel/subcategory/add/$',views.subcat_add,name='subcat_add'),
]
