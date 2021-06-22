# Generated by Django 3.2.4 on 2021-06-22 05:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spareapp', '0078_alter_reference_referencecar'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reference',
            name='referenceCar',
        ),
        migrations.RemoveField(
            model_name='reference',
            name='referenceCategory',
        ),
        migrations.RemoveField(
            model_name='reference',
            name='referenceSpare',
        ),
        migrations.AddField(
            model_name='spare',
            name='spare_reference',
            field=models.ManyToManyField(blank=True, null=True, to='spareapp.reference', verbose_name='Reference code'),
        ),
        migrations.AlterField(
            model_name='reference',
            name='referenceCode',
            field=models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='Code'),
        ),
    ]
