# Generated by Django 3.2.4 on 2021-10-17 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spareapp', '0137_factura_fechacobrado'),
    ]

    operations = [
        migrations.AlterField(
            model_name='persona',
            name='documento',
            field=models.CharField(blank=True, default='', max_length=20, null=True, verbose_name='Documento'),
        ),
    ]