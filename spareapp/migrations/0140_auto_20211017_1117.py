# Generated by Django 3.2.4 on 2021-10-17 16:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spareapp', '0139_alter_factura_num'),
    ]

    operations = [
        migrations.AlterField(
            model_name='persona',
            name='documento',
            field=models.CharField(blank=True, default='', max_length=50, null=True, verbose_name='Documento'),
        ),
        migrations.AlterField(
            model_name='persona',
            name='nombre',
            field=models.CharField(max_length=100, verbose_name='Nombre'),
        ),
    ]
