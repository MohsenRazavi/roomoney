from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse_lazy

from phonenumber_field.modelfields import PhoneNumberField


class CustomUser(AbstractUser):

    has_room = models.BooleanField(default=False)
    full_name = models.CharField(max_length=35, blank=True, null=True, default='')
    phone_number = PhoneNumberField(blank=True, null=True, default='')
    money = models.IntegerField(blank=True, null=True, default=0)
    profile_photo = models.ImageField(upload_to='users/profile', blank=True, null=True)
    biography = models.CharField(max_length=250, blank=True, null=True)

    def __str__(self):
        if self.full_name:
            return self.full_name
        return self.username

    def get_absolute_url(self):
        return reverse_lazy('roommate_view', args=[self.id])


