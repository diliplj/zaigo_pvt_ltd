# Generated by Django 4.1.5 on 2023-01-14 07:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ziago_app', '0005_members_password_alter_members_member_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='members',
            name='password',
        ),
    ]