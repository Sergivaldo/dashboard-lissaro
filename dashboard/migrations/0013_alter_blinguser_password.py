# Generated by Django 4.1.5 on 2023-01-18 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0012_keys_blinguser_keys'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blinguser',
            name='password',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
