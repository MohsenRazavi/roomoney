# Generated by Django 4.1.3 on 2022-11-11 16:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0010_purchase_sum'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='room',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='item', to='rooms.room'),
        ),
    ]
