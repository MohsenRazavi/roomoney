# Generated by Django 4.1.3 on 2022-11-13 19:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_customuser_phone_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='money',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
