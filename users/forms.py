from django.forms import ModelForm

from .models import CustomUser


class UserUpdateForm(ModelForm):
    class Meta:
        model = CustomUser
        fields = [
            'username',
            'profile_photo',
            'full_name',
            'biography',
            'email',
            'phone_number',
        ]
