# Generated by Django 4.1.2 on 2023-03-20 09:20

import django.contrib.auth.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0014_alter_workratings_customerid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='workratings',
            name='customerId',
        ),
        migrations.AddField(
            model_name='workratings',
            name='custoId',
            field=models.CharField(default=django.contrib.auth.models.User, max_length=100),
        ),
    ]
