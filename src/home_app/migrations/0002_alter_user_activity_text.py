# Generated by Django 3.2.13 on 2022-08-02 15:05

import builtins
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_activity',
            name='text',
            field=models.TextField(max_length=builtins.max),
        ),
    ]