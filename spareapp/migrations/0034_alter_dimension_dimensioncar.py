# Generated by Django 3.2.4 on 2021-06-18 20:04

from django.db import migrations
import django.db.models.deletion
import smart_selects.db_fields


class Migration(migrations.Migration):

    dependencies = [
        ('spareapp', '0033_alter_dimension_dimensioncar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dimension',
            name='dimensionCar',
            field=smart_selects.db_fields.ChainedForeignKey(blank=True, chained_field='dimensionSpare', chained_model_field='car_info', null=True, on_delete=django.db.models.deletion.CASCADE, to='spareapp.car', verbose_name='Car'),
        ),
    ]
