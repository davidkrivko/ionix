# Generated by Django 3.2.8 on 2021-10-27 10:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0024_alter_smartthermostatmodel_set_temperature'),
        ('properties', '0008_auto_20211020_0955'),
    ]

    operations = [
        migrations.AlterField(
            model_name='boilerroommodel',
            name='boiler',
            field=models.OneToOneField(blank=True, help_text='Installed boiler', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='boiler_room', to='devices.boilermodel'),
        ),
    ]
