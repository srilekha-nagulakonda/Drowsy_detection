# Generated by Django 3.2 on 2024-03-23 04:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Face_Recognition', '0006_data_status_data_submit_trips'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='trips',
            name='status',
        ),
    ]
