# Generated by Django 4.2.1 on 2023-09-06 00:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_registro', '0029_alter_confirmation_approved'),
    ]

    operations = [
        migrations.AlterField(
            model_name='state',
            name='name',
            field=models.CharField(default=None, max_length=500, null=True),
        ),
        migrations.CreateModel(
            name='Comentario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comentario', models.CharField(default=None, max_length=200000, null=True)),
                ('act_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_registro.act')),
            ],
        ),
    ]
