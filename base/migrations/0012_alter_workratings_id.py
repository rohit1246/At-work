# Generated by Django 4.1.2 on 2023-03-20 08:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0011_workratings'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workratings',
            name='id',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
    ]
