# Generated by Django 2.2.6 on 2019-10-06 16:47

import accounts.validators
from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=255, unique=True, validators=[accounts.validators.fake_email_validation])),
                ('username', models.CharField(max_length=20, unique=True)),
                ('phone', models.CharField(max_length=10, unique=True, validators=[accounts.validators.phone_number_validation])),
                ('joined', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_admin', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstName', models.CharField(default='First Name', max_length=20, verbose_name='first name')),
                ('lastName', models.CharField(default='Last Name', max_length=20, verbose_name='last name')),
                ('gender', models.CharField(choices=[('MALE', 'MALE'), ('FEMALE', 'FEMALE')], default='Gender', max_length=10, verbose_name='gender')),
                ('profileImage', models.ImageField(blank=True, null=True, upload_to='usersImages', verbose_name='profile image')),
                ('coverImage', models.ImageField(blank=True, null=True, upload_to='usersImages', verbose_name='cover image')),
                ('age', models.IntegerField(blank=True, null=True, verbose_name='age')),
                ('address', models.CharField(blank=True, default='address', max_length=100, null=True, verbose_name='addess')),
                ('pofileUsage', models.CharField(choices=[('BUY', 'BUY'), ('SELL', 'SELL'), ('BOTH', 'BOTH')], default='Profile Usage', max_length=15, verbose_name='profile usage')),
                ('profileComplete', models.BooleanField(default='False')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
