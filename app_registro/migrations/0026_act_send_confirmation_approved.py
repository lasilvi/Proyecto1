# Generated by Django 4.2.1 on 2023-08-02 19:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_registro', '0025_alter_confirmation_job_position'),
    ]

    operations = [
        migrations.AddField(
            model_name='act',
            name='send',
            field=models.BooleanField(default=None, null=True),
        ),
        migrations.AddField(
            model_name='confirmation',
            name='approved',
            field=models.BooleanField(default=None, null=True),
        ),
    ]