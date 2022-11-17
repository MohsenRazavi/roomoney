from django.contrib import admin

from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'email',
        'full_name',
        'has_room',
        'phone_number',
        # 'status'
    )
