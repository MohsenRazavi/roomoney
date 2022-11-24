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
    path('roommate_out_view/<int:pk>/', views.RoommateOutView.as_view(), name='roommate_view'),
    path('room_delete/<int:pk>/', views.room_delete_view, name='room_delete'),
    path('item_list/<int:pk>/', views.item_list_view, name='item_list'),
    path('checkout/<int:pk>/', views.checkout_view, name='checkout'),
    #
    path('notes/<int:pk>/', views.NoteListView.as_view(), name='note_list'),
    path('notes/note_delete/<int:pk>/', views.NoteDeleteView.as_view(), name='note_delete'),
    path('notes/note_create/', views.NoteCreateView.as_view(), name='note_create'),

]
