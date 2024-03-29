# Generated by Django 4.2 on 2023-08-03 07:00

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='LastEventToken',
            fields=[
                ('token', models.CharField(editable=False, primary_key=True, serialize=False, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.CharField(editable=False, max_length=128, primary_key=True, serialize=False, unique=True)),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'ordering': ['timestamp'],
            },
        ),
        migrations.CreateModel(
            name='ThreadEvent',
            fields=[
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('id', models.CharField(editable=False, max_length=128, primary_key=True, serialize=False, unique=True)),
                ('roles', models.ManyToManyField(to='event.role')),
            ],
        ),
    ]
