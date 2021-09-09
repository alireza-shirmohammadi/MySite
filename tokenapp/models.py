from __future__ import unicode_literals
from django.db import models

# Create your models here.


class Token(models.Model):

    token = models.CharField(max_length=30,default='')
    email = models.CharField(max_length=30,default='')
    def __str__(self):
        return str(self.pk)
