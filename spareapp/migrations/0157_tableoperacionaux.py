# Generated by Django 3.2.4 on 2022-01-19 22:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('spareapp', '0156_tableoperacion'),
    ]

    operations = [
        migrations.CreateModel(
            name='tableOperacionAux',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tabNombre', models.CharField(default='Principal', max_length=80, verbose_name='Nombre de tabla')),
                ('principal', models.BooleanField(blank=True, default=False, null=True, verbose_name='Principal')),
                ('suma', models.BooleanField(default=True, verbose_name='Suma')),
                ('resta', models.BooleanField(default=False, verbose_name='Resta')),
                ('tabTotal', models.FloatField(verbose_name='Total')),
                ('tabTipo', models.ForeignKey(default='Tipo', on_delete=django.db.models.deletion.CASCADE, to='spareapp.facttype', verbose_name='Tipo')),
            ],
        ),
    ]
