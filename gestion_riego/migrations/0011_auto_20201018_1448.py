# Generated by Django 3.1.1 on 2020-10-18 19:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_riego', '0010_auto_20201016_1118'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='device',
            options={'ordering': ['id'], 'verbose_name': 'Device', 'verbose_name_plural': 'Devices'},
        ),
        migrations.AlterModelOptions(
            name='historialriego',
            options={'ordering': ['-id'], 'verbose_name': 'HistorialRiego', 'verbose_name_plural': 'HistorialRiegos'},
        ),
        migrations.AlterModelOptions(
            name='persona',
            options={'ordering': ['id'], 'verbose_name': 'Persona', 'verbose_name_plural': 'Personas'},
        ),
        migrations.AlterModelOptions(
            name='planta',
            options={'ordering': ['id'], 'verbose_name': 'Planta', 'verbose_name_plural': 'Plantas'},
        ),
        migrations.AlterModelOptions(
            name='plataforma',
            options={'ordering': ['id'], 'verbose_name': 'Plataforma', 'verbose_name_plural': 'Plataformas'},
        ),
        migrations.AlterModelOptions(
            name='tiporol',
            options={'ordering': ['id'], 'verbose_name': 'TipoRol', 'verbose_name_plural': 'TipoRoles'},
        ),
        migrations.AlterModelOptions(
            name='tiposensor',
            options={'ordering': ['id'], 'verbose_name': 'TipoSensor', 'verbose_name_plural': 'TipoSensores'},
        ),
        migrations.AlterModelOptions(
            name='tiposuelo',
            options={'ordering': ['id'], 'verbose_name': 'TipoSuelo', 'verbose_name_plural': 'TipoSuelos'},
        ),
    ]