# Generated by Django 3.2.4 on 2021-09-15 18:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spareapp', '0123_factcategory_facttype_factura_persona'),
    ]

    operations = [
        migrations.AlterField(
            model_name='factcategory',
            name='ingreso',
            field=models.BooleanField(default=False, verbose_name='Ingreso'),
        ),
    ]
