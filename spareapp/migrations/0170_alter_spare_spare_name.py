# Generated by Django 4.0.4 on 2023-04-07 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spareapp', '0169_alter_spare_spare_brand_alter_spare_spare_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='spare',
            name='spare_name',
            field=models.CharField(blank=True, max_length=400, null=True, verbose_name='Description'),
        ),
    ]
