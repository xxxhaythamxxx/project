# Generated by Django 4.0.4 on 2023-02-24 16:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spareapp', '0164_alter_car_car_model'),
    ]

    operations = [
        migrations.AddField(
            model_name='engine',
            name='engine_manufacturer',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='Manufacturer'),
        ),
    ]
