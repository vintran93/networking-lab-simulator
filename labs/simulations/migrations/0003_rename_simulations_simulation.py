# Generated by Django 5.2.3 on 2025-06-23 01:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('simulations', '0002_rename_card_simulations'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Simulations',
            new_name='Simulation',
        ),
    ]
