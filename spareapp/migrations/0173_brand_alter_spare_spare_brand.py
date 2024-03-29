# Generated by Django 4.0.4 on 2023-05-23 03:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('spareapp', '0172_manufacturer_alter_car_car_manufacturer'),
    ]

    operations = [
        migrations.CreateModel(
            name='brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand', models.CharField(blank=True, max_length=100, null=True, verbose_name='Brand')),
            ],
            options={
                'verbose_name_plural': 'Brands',
            },
        ),
        migrations.AlterField(
            model_name='spare',
            name='spare_brand',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='spareapp.brand', verbose_name='Brand'),
        ),
    ]
