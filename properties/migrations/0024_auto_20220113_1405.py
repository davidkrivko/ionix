# Generated by Django 3.2.9 on 2022-01-13 19:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0023_weatherrecordmodel_temp'),
    ]

    operations = [
        migrations.RenameField(
            model_name='weatherrecordmodel',
            old_name='temp',
            new_name='temp_f',
        ),
        migrations.AddField(
            model_name='weatherrecordmodel',
            name='temp_c',
            field=models.IntegerField(blank=True, help_text='Temp value from weather.gov API in °C', null=True),
        ),
    ]
