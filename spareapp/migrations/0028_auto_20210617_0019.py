# Generated by Django 3.2.4 on 2021-06-17 00:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('spareapp', '0027_auto_20210611_2213'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='car',
            name='car_from',
        ),
        migrations.RemoveField(
            model_name='car',
            name='car_to',
        ),
    ]
