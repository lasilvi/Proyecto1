# Generated by Django 4.2.1 on 2023-09-16 21:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_registro', '0032_alter_act_hour_alter_act_next_hour_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='contraseña',
            field=models.CharField(default=None, max_length=200),
        ),
    ]
