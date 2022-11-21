# Generated by Django 4.1.3 on 2022-11-21 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0017_alter_item_description'),
    ]

    operations = [
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150)),
                ('text', models.TextField()),
                ('datetime_create', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]