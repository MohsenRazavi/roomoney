# Generated by Django 4.1.3 on 2022-11-05 10:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchase',
            name='title',
            field=models.CharField(blank=True, max_length=250),
        ),
    ]