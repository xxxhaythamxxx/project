# Generated by Django 4.0.4 on 2023-03-28 00:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spareapp', '0165_engine_engine_manufacturer'),
    ]

    operations = [
        migrations.AddField(
            model_name='car',
            name='chasis',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='Chasis'),
        ),
        migrations.AlterField(
            model_name='car',
            name='transmission',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='Transmision'),
        ),
    ]
