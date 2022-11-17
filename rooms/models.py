from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse


class Room(models.Model):
    BUILDING_CHOICES = (
        ('Mofateh', 'Mofateh'),
        ('Chamran', 'Chamran'),
    )
    created_at = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(get_user_model(), null=True, on_delete=models.CASCADE, related_name='created_room')
    name = models.CharField(max_length=100, blank=False, verbose_name='Room name')
    building = models.CharField(choices=BUILDING_CHOICES, max_length=7, blank=False)
    room_number = models.DecimalField(max_digits=3, decimal_places=0, default=100)
    description = models.TextField(blank=True)
    member = models.ManyToManyField(get_user_model(), related_name='room')

    def __str__(self):
        return f"<{self.name}, {self.building}, {self.room_number}>"

    def get_absolute_url(self):
        return reverse('room_options', args=[self.id])


class Item(models.Model):
    name = models.CharField(max_length=50, blank=False)
    price = models.DecimalField(max_digits=9, decimal_places=0, default=0, blank=False)
    in_purchase = models.BooleanField(default=False)
    room = models.ForeignKey(Room, related_name='item', on_delete=models.CASCADE)
    datetime_bought = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f'<{self.name}, {self.price}>'


class Purchase(models.Model):
    title = models.CharField(max_length=250, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    purchaser = models.ForeignKey(get_user_model(), related_name='purchase', on_delete=models.CASCADE, blank=False)
    items = models.ManyToManyField(Item, related_name='cart')
    member = models.ManyToManyField(get_user_model(), related_name='shared_purchase', blank=True)
    is_payed = models.BooleanField(default=False)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='purchases', null=True)
    sum = models.PositiveIntegerField(null=True)

    def __str__(self):
        return f"<{self.title}, {self.items}>"

    def calculate_sum(self):
        res = 0
        for item in self.items.all():
            res += item.price
        self.sum = res
        self.save()
        return res
