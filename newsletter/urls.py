from django.conf.urls import url

from . import views

urlpatterns = [
    url(r"^newsletter/add/$", views.news_letter, name="news_letter"),
    url(r"^panel/newsletter/emails/$", views.news_email, name="news_email"),
    url(
        r"^panel/newsletter/del/(?P<pk>\d+)/$", views.news_txt_del, name="news_txt_del"
    ),
    url(r"^panel/newsletter/answer/$", views.news_letter_ans, name="news_letter_ans"),
]
