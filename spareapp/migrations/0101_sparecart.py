# Generated by Django 3.2.4 on 2021-09-02 13:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spareapp', '0100_spare_note'),
    ]

    operations = [
        migrations.CreateModel(
            name='spareCart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('spareCode', models.CharField(blank=True, max_length=20, null=True, unique=True, verbose_name='Code')),
                ('nameUser', models.CharField(blank=True, max_length=20, null=True, unique=True, verbose_name='User')),
            ],
        ),
    ]