from django.forms import ModelForm

from .models import CustomUser


class UserUpdateForm(ModelForm):
    class Meta:
        model = CustomUser
        fields = [
            'username',
            'full_name',
            'email',
            'phone_number',
        ]
