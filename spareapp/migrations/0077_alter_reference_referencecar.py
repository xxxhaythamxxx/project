# Generated by Django 3.2.4 on 2021-06-22 04:24

from django.db import migrations, models
import django.db.models.deletion
import smart_selects.db_fields


class Migration(migrations.Migration):

    dependencies = [
        ('spareapp', '0076_alter_reference_referencecar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reference',
            name='referenceCar',
            field=models.ForeignKey(blank=True, limit_choices_to={'spare__id': smart_selects.db_fields.ChainedForeignKey(blank=True, chained_field='referenceCategory', chained_model_field='spare_category', null=True, on_delete=django.db.models.deletion.CASCADE, to='spareapp.spare', verbose_name='Spare')}, null=True, on_delete=django.db.models.deletion.CASCADE, to='spareapp.car', verbose_name='Car'),
        ),
    ]
