# Generated by Django 3.2.4 on 2021-09-25 02:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spareapp', '0132_persona_documento'),
    ]

    operations = [
        migrations.AlterField(
            model_name='factcategory',
            name='nombre',
            field=models.CharField(blank=True, max_length=40, null=True, verbose_name='Categoría'),
        ),
        migrations.AlterField(
            model_name='facttype',
            name='nombre',
            field=models.CharField(default='Tipo', max_length=40, verbose_name='Tipo'),
        ),
    ]
