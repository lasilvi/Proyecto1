# Generated by Django 4.2.1 on 2023-09-06 13:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_registro', '0030_alter_state_name_comentario'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commitment',
            name='control',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_registro.state'),
        ),
        migrations.AlterField(
            model_name='commitment',
            name='observations',
            field=models.CharField(max_length=20000),
        ),
        migrations.AlterField(
            model_name='commitment',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_registro.user'),
        ),
        migrations.AlterField(
            model_name='development',
            name='discussion',
            field=models.CharField(max_length=20000, null=True),
        ),
        migrations.AlterField(
            model_name='development',
            name='result',
            field=models.CharField(max_length=20000, null=True),
        ),
    ]
