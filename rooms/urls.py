from django.urls import path

from . import views

urlpatterns = [
    path('', views.room_home_view, name='room_dashboard'),
    path('options/<int:pk>/', views.RoomOptionsView.as_view(), name='room_options'),
]
