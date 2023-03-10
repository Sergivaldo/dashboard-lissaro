# Generated by Django 4.1.5 on 2023-01-15 04:42

import dashboard.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ApiData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bank_accounts', models.TextField()),
                ('payments', models.TextField()),
                ('receivements', models.TextField()),
                ('updated_at', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='BlingUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(max_length=65, null=True, unique=True)),
                ('password', models.CharField(max_length=65, null=True)),
                ('api_key', models.CharField(max_length=255, null=True)),
                ('api_data', models.OneToOneField(default=dashboard.models.ApiData, null=True, on_delete=django.db.models.deletion.SET_NULL, to='dashboard.apidata')),
                ('dashboard_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
