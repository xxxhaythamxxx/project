# Generated by Django 4.0.4 on 2022-11-30 23:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spareapp', '0163_subcategory_spare_spare_subcategory'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='car_model',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Model'),
        ),
    ]
