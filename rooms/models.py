from django.db import models
from django.contrib.auth import get_user_model


class Item(models.Model):
    name = models.CharField(max_length=50, blank=False)
    price = models.DecimalField(max_digits=9, decimal_places=0, default=0, blank=False)

    def __str__(self):
        return f'<{self.name}, {self.price}>'


class Room(models.Model):
    BUILDING_CHOICES = (
        ('Mofateh', 'Mofateh'),
        ('Chamran', 'Chamran'),
    )
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100, blank=False)
    building = models.CharField(choices=BUILDING_CHOICES, max_length=7, blank=False)
    room_number = models.DecimalField(max_digits=3, decimal_places=0, default=100)
    description = models.TextField(blank=True)
    member = models.ManyToManyField(get_user_model(), related_name='room')

    def __str__(self):
        return f"<{self.name}, {self.building}, {self.room_number}>"


class Purchase(models.Model):
    title = models.CharField(max_length=250, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    purchaser = models.ForeignKey(get_user_model(), related_name='purchase', on_delete=models.CASCADE, blank=False)
    items = models.ManyToManyField(Item, related_name='cart')
    member = models.ManyToManyField(get_user_model(), related_name='shared_purchase', blank=True)
    is_payed = models.BooleanField(default=False)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='purchases', null=True)

    def __str__(self):
        return self.title
