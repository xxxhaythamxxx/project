# Generated by Django 3.2.3 on 2021-06-04 22:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spareapp', '0023_auto_20210604_1810'),
    ]

    operations = [
        migrations.AlterField(
            model_name='spare',
            name='spare_reference',
            field=models.ManyToManyField(blank=True, null=True, to='spareapp.reference', verbose_name='Reference code'),
        ),
        migrations.AlterField(
            model_name='spare',
            name='spare_spare',
            field=models.ManyToManyField(blank=True, null=True, related_name='_spareapp_spare_spare_spare_+', to='spareapp.spare', verbose_name='Spare target'),
        ),
    ]
