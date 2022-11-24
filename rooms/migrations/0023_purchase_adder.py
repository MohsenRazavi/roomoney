# Generated by Django 4.1.3 on 2022-11-24 08:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('rooms', '0022_alter_purchase_member'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchase',
            name='adder',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='add_purchases', to=settings.AUTH_USER_MODEL),
        ),
    ]
