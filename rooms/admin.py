from django.contrib import admin

from .models import Item, Purchase, Room

admin.site.register(Item)


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        'purchaser',
        'room',
        'is_payed'
    )


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'building',
        'room_number',
    )
