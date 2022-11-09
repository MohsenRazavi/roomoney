from django.urls import path

from . import views

urlpatterns = [
    path('', views.room_home_view, name='room_dashboard'),
    path('options/<int:pk>/', views.RoomOptionsView.as_view(), name='room_options'),
    path('new_purchase/', views.add_new_purchase, name='new_purchase'),
    path('add_item_to_purchase/', views.add_item_to_purchase, name='add_to_purchase')
]
