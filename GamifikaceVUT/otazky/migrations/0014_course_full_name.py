# Generated by Django 5.0.1 on 2024-04-08 22:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('otazky', '0013_remove_course_full_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='full_name',
            field=models.CharField(default='', max_length=255),
        ),
    ]
