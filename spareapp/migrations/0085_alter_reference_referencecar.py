# Generated by Django 3.2.4 on 2021-06-22 21:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spareapp', '0084_alter_reference_referencecar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reference',
            name='referenceCar',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Code'),
        ),
    ]
