# Generated by Django 3.2.4 on 2021-09-22 21:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spareapp', '0130_factura_pendiente'),
    ]

    operations = [
        migrations.AddField(
            model_name='factura',
            name='total',
            field=models.FloatField(default=0, verbose_name='Total'),
        ),
    ]
