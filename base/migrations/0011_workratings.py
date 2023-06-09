# Generated by Django 4.1.2 on 2023-03-19 20:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('base', '0010_personalinfo_profile_pic'),
    ]

    operations = [
        migrations.CreateModel(
            name='workRatings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('professionalId', models.CharField(max_length=100)),
                ('electricianRating', models.CharField(max_length=20, null=True)),
                ('plumberRating', models.CharField(max_length=20, null=True)),
                ('painterRating', models.CharField(max_length=20, null=True)),
                ('carrepairRating', models.CharField(max_length=20, null=True)),
                ('tailorRating', models.CharField(max_length=20, null=True)),
                ('transportRating', models.CharField(max_length=20, null=True)),
                ('tutorRating', models.CharField(max_length=20, null=True)),
                ('customerId', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, unique=True)),
            ],
        ),
    ]
