from django.urls import path, include

from . import views

urlpatterns = [
    path('update_profile/<int:pk>/', views.UserUpdateView.as_view(), name='profile_update'),
    path('leave_room/', views.leave_room_view, name='leave_room'),
]
