# Generated by Django 3.1.1 on 2021-01-17 19:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_riego', '0004_auto_20210117_1909'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historialriego',
            name='image_1_variable',
            field=models.ImageField(blank=True, null=True, upload_to='fuzzy1'),
        ),
        migrations.AlterField(
            model_name='historialriego',
            name='image_3_variable',
            field=models.ImageField(blank=True, null=True, upload_to='fuzzy3'),
        ),
        migrations.AlterField(
            model_name='historialriego',
            name='image_4_variable',
            field=models.ImageField(blank=True, null=True, upload_to='fuzzy4'),
        ),
    ]
