from django.contrib import admin
from django.conf.urls import url,include
from . import views
urlpatterns = [
    url(r'^token/$', views.token, name='token'),
]
