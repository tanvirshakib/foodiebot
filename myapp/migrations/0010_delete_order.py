# Generated by Django 5.0.6 on 2024-07-25 07:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0009_customerorder_delivery_time'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Order',
        ),
    ]
