# Generated by Django 3.2.8 on 2021-10-12 12:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
        ('devices', '0001_initial'),
        ('properties', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='smartthermostatmodel',
            name='owner',
            field=models.ForeignKey(blank=True, help_text='Related property Owner', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='smart_thermostats', related_query_name='smart_thermostat', to='users.ownerprofilemodel'),
        ),
        migrations.AddField(
            model_name='smartthermostatmodel',
            name='zone',
            field=models.ForeignKey(blank=True, help_text='Related property Zone', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='smart_thermostats', related_query_name='smart_thermostat', to='properties.zonemodel'),
        ),
        migrations.AddField(
            model_name='sensormodel',
            name='boiler',
            field=models.ForeignKey(blank=True, help_text='Boiler object (if connected)', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sensors', related_query_name='sensor', to='devices.boilermodel'),
        ),
        migrations.AddField(
            model_name='sensormodel',
            name='parent_device',
            field=models.ForeignKey(help_text='Parent controller', on_delete=django.db.models.deletion.CASCADE, related_name='sensors', related_query_name='sensor', to='devices.ioniqcontrollermodel'),
        ),
        migrations.AddField(
            model_name='sensormodel',
            name='zone',
            field=models.ForeignKey(blank=True, help_text='Related property Zone', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sensors', related_query_name='sensor', to='properties.zonemodel'),
        ),
        migrations.AddField(
            model_name='ioniqcontrollermodel',
            name='boiler',
            field=models.ForeignKey(blank=True, help_text='Connected Boiler', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='ioniq_controllers', related_query_name='ioniq_controller', to='devices.boilermodel'),
        ),
        migrations.AddField(
            model_name='ioniqcontrollermodel',
            name='owner',
            field=models.ForeignKey(blank=True, help_text='Related property Owner', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='ioniq_controllers', related_query_name='ioniq_controller', to='users.ownerprofilemodel'),
        ),
        migrations.AddField(
            model_name='boilermodel',
            name='owner',
            field=models.ForeignKey(blank=True, help_text='Related property Owner', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='boilers', related_query_name='boiler', to='users.ownerprofilemodel'),
        ),
        migrations.AddField(
            model_name='analoguethermostatmodel',
            name='zone',
            field=models.ForeignKey(help_text='Related Heating Zone', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='analogue_thermostats', related_query_name='analogue_thermostat', to='properties.zonemodel'),
        ),
    ]
