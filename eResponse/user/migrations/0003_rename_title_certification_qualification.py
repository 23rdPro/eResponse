# Generated by Django 4.2 on 2023-07-31 07:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_alter_user_managers'),
    ]

    operations = [
        migrations.RenameField(
            model_name='certification',
            old_name='title',
            new_name='qualification',
        ),
    ]
