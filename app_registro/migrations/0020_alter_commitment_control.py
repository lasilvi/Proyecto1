# Generated by Django 4.2.1 on 2023-07-07 19:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_registro', '0019_alter_commitment_control'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commitment',
            name='control',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='app_registro.state'),
        ),
    ]