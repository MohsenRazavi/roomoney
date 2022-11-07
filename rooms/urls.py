from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.room_home_view, name='room_dashboard'),
]
