# Generated by Django 4.1.5 on 2023-01-12 16:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ziago_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='members',
            table='Member',
        ),
        migrations.AlterModelTable(
            name='rights',
            table='Right',
        ),
        migrations.AlterModelTable(
            name='roles',
            table='Role',
        ),
    ]