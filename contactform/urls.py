from django.conf.urls import url

from . import views

urlpatterns = [
    url(r"^contact/submit/$", views.contact_add, name="contact_add"),
    url(r"^panel/contactform/$", views.contact_show, name="contact_show"),
    url(r"^panel/contactform/del/(?P<pk>\d+)/$", views.contact_del, name="contact_del"),
    url(r"^contactform/answer/(?P<pk>\d+)/$", views.contact_ans, name="contact_ans"),
]
