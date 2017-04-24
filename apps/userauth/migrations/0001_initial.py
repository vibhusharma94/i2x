# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-23 13:58
from __future__ import unicode_literals

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(max_length=55, verbose_name='first name')),
                ('last_name', models.CharField(max_length=55, verbose_name='last name')),
                ('email', models.EmailField(max_length=255, unique=True)),
                ('is_staff', models.BooleanField(default=False, help_text='Admin access allowed?', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='User is active and is not Blocked?', verbose_name='active')),
                ('is_verified', models.BooleanField(default=False, help_text='User email is verified?', verbose_name='verified')),
                ('date_joined', models.DateTimeField(default=datetime.datetime.now, verbose_name='date joined')),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'User',
                'verbose_name_plural': 'Users',
            },
        ),
        migrations.CreateModel(
            name='AccountActivation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('activation_key', models.CharField(max_length=255, unique=True)),
                ('created', models.DateTimeField(default=datetime.datetime.now, verbose_name='created at')),
                ('is_active', models.BooleanField(default=True, verbose_name='link still active')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='email_verification', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'email verification',
                'verbose_name_plural': 'email verifications',
            },
        ),
        migrations.CreateModel(
            name='CustomToken',
            fields=[
                ('key', models.CharField(max_length=40, primary_key=True, serialize=False, verbose_name='Key')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('expiry_time', models.DateTimeField(default=datetime.datetime.now)),
                ('refresh_token', models.CharField(blank=True, max_length=40, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='auth_token', to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'abstract': False,
                'verbose_name': 'API Authentication Token',
                'verbose_name_plural': 'API Authentication Tokens',
            },
        ),
        migrations.CreateModel(
            name='PasswordReset',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reset_key', models.CharField(max_length=100, unique=True, verbose_name='reset_key')),
                ('created', models.DateTimeField(default=datetime.datetime.now, verbose_name='created at')),
                ('is_active', models.BooleanField(default=True, verbose_name='link still active')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
            options={
                'verbose_name': 'password reset',
                'verbose_name_plural': 'password resets',
            },
        ),
    ]
