# Generated by Django 3.2.4 on 2021-07-15 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spareapp', '0098_alter_engine_engine_cylinder'),
    ]

    operations = [
        migrations.AddField(
            model_name='reference',
            name='referenceNote',
            field=models.CharField(blank=True, max_length=40, null=True, verbose_name='Note'),
        ),
    ]
