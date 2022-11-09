from django import forms
from django.forms import ModelForm
from django.forms.widgets import CheckboxSelectMultiple
from django.contrib.auth import get_user_model

from .models import Room, Purchase, Item


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


class NewPurchaseForm(ModelForm):
    class Meta:
        model = Purchase
        fields = [
            'title',
            'purchaser',
            'items',
            'member',
        ]

    def __init__(self, room, *args, **kwargs):
        super(NewPurchaseForm, self).__init__(*args, **kwargs)

        self.fields['member'].widget = CheckboxSelectMultiple()
        self.fields['member'].queryset = get_user_model().objects.filter(room=room)
        self.fields['items'].widget = CheckboxSelectMultiple()
        self.fields['items'].queryset = Item.objects.filter(in_purchase=False)
        self.fields['purchaser'].queryset = get_user_model().objects.filter(room=room)


class ItemCreateForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = [
            'name',
            'price'
        ]
