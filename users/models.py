from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse_lazy

from phonenumber_field.modelfields import PhoneNumberField


class CustomUser(AbstractUser):
    # STATUS_CHOICES = (
    #     ("none", "none"),
    #     ("debtor", "debtor"),
    #     ("creditor", "creditor"),
    # )
    # profile = models.ImageField()
    has_room = models.BooleanField(default=False)
    # status = models.CharField(choices=STATUS_CHOICES, max_length=8, default=STATUS_CHOICES[0][0])
    full_name = models.CharField(max_length=35, blank=True, null=True, default='')
    phone_number = PhoneNumberField(blank=True, null=True, default='')
    money = models.IntegerField(blank=True, null=True, default=0)

    def __str__(self):
        if self.full_name:
            return self.full_name
        return self.username

    def get_absolute_url(self):
        return reverse_lazy('roommate_view', args=[self.id])


