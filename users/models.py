from django.db import models
from django.contrib.auth.models import AbstractUser

from phonenumber_field.modelfields import PhoneNumberField


class CustomUser(AbstractUser):
    STATUS_CHOICES = (
        ("none", "none"),
        ("debtor", "debtor"),
        ("creditor", "creditor"),
    )
    # profile = models.ImageField()
    has_room = models.BooleanField(default=False)
    status = models.CharField(choices=STATUS_CHOICES, max_length=8, default=STATUS_CHOICES[0][0])
    full_name = models.CharField(max_length=35, blank=True, null=True)
    phone_number = PhoneNumberField(blank=True, null=True)


