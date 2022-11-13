from django.urls import path

from . import views

urlpatterns = [
    path('', views.room_home_view, name='room_dashboard'),
    path('options/<int:pk>/', views.RoomOptionsView.as_view(), name='room_options'),
    path('new_purchase/', views.add_new_purchase, name='new_purchase'),
    path('add_item_to_purchase/', views.add_item_to_purchase, name='add_to_purchase'),
    path('delete_item_from_purchase/<int:pk>/', views.DeleteItemFromPurchase.as_view(), name='delete_item_from_purchase'),
    path('purchase_list/<int:pk>/', views.purchase_list_view, name='purchase_list'),
    path('delete_purchase/<int:pk>/', views.PurchaseDeleteView.as_view(), name='delete_purchase'),
    path('update_purchase/<int:pk>/', views.PurchaseUpdateView.as_view(), name='update_purchase'),

]
