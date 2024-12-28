from os import name
from django.contrib import admin
from django.urls import path
from .views import register,login,home,account_settings

urlpatterns = [
    path('register/',register,name='register'),
    path('login/',login,name='login'),
    path('settings/',account_settings,name='account_settings'),
    path('',home,name='home')
]
