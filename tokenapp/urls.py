from django.conf.urls import url

from . import views

urlpatterns = [
    url(r"^token/$", views.token, name="token"),
]
