# Generated by Django 3.2.4 on 2021-07-15 15:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spareapp', '0099_reference_referencenote'),
    ]

    operations = [
        migrations.AddField(
            model_name='spare',
            name='note',
            field=models.TextField(blank=True, max_length=100, null=True, verbose_name='Note'),
        ),
    ]
