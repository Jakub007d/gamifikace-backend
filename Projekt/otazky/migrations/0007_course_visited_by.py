# Generated by Django 5.0.1 on 2024-04-08 21:47

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('otazky', '0006_rename_okruh_chalangequestion_courseid'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='visited_by',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]
