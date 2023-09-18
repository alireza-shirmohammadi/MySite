"""mag URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from django.views.static import serve
from rest_framework import routers

from main import views

router = routers.DefaultRouter()
router.register(r"^magnews", views.NewsViewSet)
urlpatterns = [
    url("admin/", admin.site.urls),
    url(r"rest/", include(router.urls)),
    url(r"api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    url(r"^media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT}),
    url(r"^static/(?P<path>.*)$", serve, {"document_root": settings.STATIC_ROOT}),
    url("", include("main.urls")),
    url("", include("news.urls")),
    url("", include("cat.urls")),
    url("", include("subcat.urls")),
    url("", include("contactform.urls")),
    url("", include("trending.urls")),
    url("", include("manager.urls")),
    url("", include("newsletter.urls")),
    url("", include("comment.urls")),
    url("", include("blacklist.urls")),
    url("", include("tokenapp.urls")),
    url("", include("search.urls")),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
