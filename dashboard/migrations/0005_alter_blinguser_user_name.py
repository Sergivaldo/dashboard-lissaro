# Generated by Django 4.1.5 on 2023-01-15 19:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0004_apidata_bling_user_alter_blinguser_api_data'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blinguser',
            name='user_name',
            field=models.CharField(max_length=65, null=True),
        ),
    ]
