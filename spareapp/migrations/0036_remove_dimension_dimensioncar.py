# Generated by Django 3.2.4 on 2021-06-18 20:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('spareapp', '0035_alter_dimension_dimensioncar'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dimension',
            name='dimensionCar',
        ),
    ]
