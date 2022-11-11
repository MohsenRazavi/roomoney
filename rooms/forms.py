from django import forms
from django.forms import ModelForm
from django.forms.widgets import CheckboxSelectMultiple

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
        widgets = {
            'items': CheckboxSelectMultiple(),
            'member': CheckboxSelectMultiple(),
        }


class ItemCreateForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = [
            'name',
            'price'
        ]
