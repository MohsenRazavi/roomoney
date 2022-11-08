from django.forms import ModelForm

from .models import CustomUser


class UserUpdateForm(ModelForm):
    class Meta:
        model = CustomUser
        fields = [
            'username',
            'first_name',
            'last_name',
            'full_name',
            'email',
            'phone_number'
        ]
