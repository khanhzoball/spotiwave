from operator import mod
from os import access
from pyexpat import model
from django.db import models

class Token(models.Model):
    user_id = models.CharField(max_length=200)
    created_at = models.DateField(auto_now_add=True)
    access_token = models.CharField(max_length=200)
    refresh_token = models.CharField(max_length=200)
    expires_in = models.DateTimeField(max_length=200)
