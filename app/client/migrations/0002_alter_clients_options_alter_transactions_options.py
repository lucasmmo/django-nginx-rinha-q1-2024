# Generated by Django 5.0.2 on 2024-02-23 12:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='clients',
            options={'managed': False, 'verbose_name': 'client', 'verbose_name_plural': 'clients'},
        ),
        migrations.AlterModelOptions(
            name='transactions',
            options={'managed': False, 'verbose_name': 'transaction', 'verbose_name_plural': 'transactions'},
        ),
    ]