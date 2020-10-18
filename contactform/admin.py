from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import ContactForm
from django.contrib.auth.models import Permission

# Register your models here.

admin.site.register(ContactForm)
