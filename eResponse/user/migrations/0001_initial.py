# Generated by Django 4.2 on 2023-07-09 07:46

from django.db import migrations, models
import eResponse.user.managers
import eResponse.user.models
import phonenumber_field.modelfields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Certification',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('title', models.CharField(max_length=128, verbose_name='Title')),
                ('description', models.TextField(max_length=555, verbose_name='Describe achievement')),
                ('upload', models.FileField(blank=True, null=True, upload_to=eResponse.user.models.cert_path)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('is_active', models.BooleanField(default=False, verbose_name='Active Status')),
                ('is_available', models.BooleanField(default=True, verbose_name='Availability')),
                ('is_superuser', models.BooleanField(default=False, verbose_name='Superuser')),
                ('is_staff', models.BooleanField(default=False, verbose_name='Admin')),
                ('title', models.CharField(blank=True, max_length=128, verbose_name='Title')),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='Email Address')),
                ('name', models.CharField(blank=True, max_length=128, verbose_name='Full Name')),
                ('mobile', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, region=None)),
                ('avatar', models.FileField(blank=True, upload_to=eResponse.user.models.avatars_path)),
                ('certifications', models.ManyToManyField(related_name='certificates', to='user.certification')),
                ('groups', models.ManyToManyField(related_name='groups', to='auth.group')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'ordering': ['created_at'],
            },
            managers=[
                ('objects', eResponse.user.managers.UserManager()),
            ],
        ),
    ]