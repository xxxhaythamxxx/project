# Generated by Django 4.0.4 on 2023-04-07 16:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spareapp', '0167_transmission_remove_car_transmission_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='spare',
            name='spare_code',
            field=models.CharField(blank=True, max_length=40, null=True, unique=True, verbose_name='Code'),
        ),
    ]
