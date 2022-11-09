"""

config URL Configuration

"""
from allauth.account import views
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', views.login),
    path('room/', include('rooms.urls')),
    path('users/', include('users.urls')),

]
