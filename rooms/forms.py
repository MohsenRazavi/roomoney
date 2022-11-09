from django.forms import ModelForm

from .models import Room


class RoomCreateForm(ModelForm):
    class Meta:
        model = Room
        fields = [
            'name',
            'description',
            'building',
            'room_number',
        ]


class RoomOptionsForm(ModelForm):
    class Meta:
        model = Room
        fields = [
            'name',
            'description',
            'building',
            'room_number',
            'member',
        ]
