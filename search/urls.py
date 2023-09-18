from django.conf.urls import url
from django.urls import path

from . import views

urlpatterns = [
    url("^search/news/$", views.search, name="search"),
    path("search_api", views.search_api, name="search_api"),
]
