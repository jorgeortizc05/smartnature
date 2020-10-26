# Generated by Django 3.1.1 on 2020-10-25 22:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_riego', '0015_auto_20201025_1746'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='plataforma',
            name='planta',
        ),
        migrations.AddField(
            model_name='plataforma',
            name='persona',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='gestion_riego.persona'),
        ),
    ]
