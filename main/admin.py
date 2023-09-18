# Register your models here.
from django.contrib import admin
from django.contrib.auth.models import Permission

from .models import Main

# Register your models here.

admin.site.register(Main)
admin.site.register(Permission)
