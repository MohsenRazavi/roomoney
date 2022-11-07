# Generated by Django 4.1.3 on 2022-11-05 12:23

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('rooms', '0002_purchase_title'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='room',
            name='member',
        ),
        migrations.AddField(
            model_name='room',
            name='member',
            field=models.ManyToManyField(related_name='room', to=settings.AUTH_USER_MODEL),
        ),
    ]
