# Generated by Django 3.2 on 2024-03-25 15:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Face_Recognition', '0012_auto_20240325_2032'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='trips',
            name='Trip_status',
        ),
    ]
