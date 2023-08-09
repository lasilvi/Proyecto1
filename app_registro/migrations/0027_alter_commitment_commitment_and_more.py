# Generated by Django 4.2.1 on 2023-08-08 22:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_registro', '0026_act_send_confirmation_approved'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commitment',
            name='commitment',
            field=models.CharField(max_length=200000),
        ),
        migrations.AlterField(
            model_name='commitment',
            name='observations',
            field=models.CharField(default=None, max_length=20000, null=True),
        ),
        migrations.AlterField(
            model_name='development',
            name='description',
            field=models.CharField(default=None, max_length=20000, null=True),
        ),
        migrations.AlterField(
            model_name='development',
            name='discussion',
            field=models.CharField(default=None, max_length=20000, null=True),
        ),
        migrations.AlterField(
            model_name='development',
            name='result',
            field=models.CharField(default=None, max_length=20000, null=True),
        ),
        migrations.AlterField(
            model_name='development',
            name='tittle',
            field=models.CharField(default=None, max_length=2000, null=True),
        ),
    ]