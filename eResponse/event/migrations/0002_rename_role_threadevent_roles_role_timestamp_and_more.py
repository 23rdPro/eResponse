# Generated by Django 4.2 on 2023-04-06 07:55

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='threadevent',
            old_name='role',
            new_name='roles',
        ),
        migrations.AddField(
            model_name='role',
            name='timestamp',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='role',
            name='id',
            field=models.BigIntegerField(editable=False, primary_key=True, serialize=False, unique=True),
        ),
    ]