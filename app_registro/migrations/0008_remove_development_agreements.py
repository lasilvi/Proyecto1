# Generated by Django 4.2.1 on 2023-06-08 00:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_registro', '0007_development_num'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='development',
            name='agreements',
        ),
    ]
