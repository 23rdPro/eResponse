# Generated by Django 4.2 on 2023-04-15 19:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0003_remove_role_role_alter_role_id_alter_threadevent_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='LastEventToken',
            fields=[
                ('token', models.CharField(editable=False, primary_key=True, serialize=False, unique=True)),
            ],
        ),
    ]