from django.contrib import admin
from django.urls import path, include
from .views import login, access_token_request, retrieve_info

urlpatterns = [
   path('v1/login', login),
   path('v1/access-token-request', access_token_request),
   path('v1/retrieve-info', retrieve_info)
]

