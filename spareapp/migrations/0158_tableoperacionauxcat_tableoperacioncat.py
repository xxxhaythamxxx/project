# Generated by Django 3.2.4 on 2022-01-30 18:51

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('spareapp', '0157_tableoperacionaux'),
    ]

    operations = [
        migrations.CreateModel(
            name='tableOperacionCat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Fecha')),
                ('tabNombre', models.CharField(default='Principal', max_length=80, verbose_name='Nombre de tabla')),
                ('principal', models.BooleanField(blank=True, default=False, null=True, verbose_name='Principal')),
                ('suma', models.BooleanField(default=True, verbose_name='Suma')),
                ('resta', models.BooleanField(default=False, verbose_name='Resta')),
                ('tabTotal', models.FloatField(verbose_name='Total')),
                ('tabCat', models.ForeignKey(default='Categoria', on_delete=django.db.models.deletion.CASCADE, to='spareapp.factcategory', verbose_name='Categoria')),
            ],
        ),
        migrations.CreateModel(
            name='tableOperacionAuxCat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tabNombre', models.CharField(default='Principal', max_length=80, verbose_name='Nombre de tabla')),
                ('principal', models.BooleanField(blank=True, default=False, null=True, verbose_name='Principal')),
                ('suma', models.BooleanField(default=True, verbose_name='Suma')),
                ('resta', models.BooleanField(default=False, verbose_name='Resta')),
                ('tabTotal', models.FloatField(verbose_name='Total')),
                ('tabCat', models.ForeignKey(default='Categoria', on_delete=django.db.models.deletion.CASCADE, to='spareapp.factcategory', verbose_name='Categoria')),
            ],
        ),
    ]
