# Generated by Django 4.1.3 on 2022-11-05 12:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0006_remove_purchase_member_purchase_member'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='room',
            name='purchases',
        ),
        migrations.AddField(
            model_name='purchase',
            name='room',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='purchases', to='rooms.room'),
        ),
    ]