# Generated by Django 4.1.5 on 2023-01-17 17:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0009_remove_apidata_api_data_alter_apidata_bling_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apidata',
            name='bling_user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='dashboard.blinguser'),
        ),
    ]
