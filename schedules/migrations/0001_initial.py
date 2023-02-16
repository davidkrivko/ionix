# Generated by Django 3.2.9 on 2021-11-03 10:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('devices', '0027_auto_20211031_1814'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeviceScheduleModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('checkpoint', models.DateTimeField(help_text='Primary timestamp for scheduled execution')),
            ],
            options={
                'verbose_name': 'Schedule window',
                'verbose_name_plural': 'Schedule windows',
                'ordering': ['checkpoint'],
            },
        ),
        migrations.CreateModel(
            name='ThermostatSubscriberModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('schedule', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='subscribers', related_query_name='subscriber', to='schedules.deviceschedulemodel')),
                ('thermostat', models.ForeignKey(help_text='Smart thermostat which should be updated', null=True, on_delete=django.db.models.deletion.CASCADE, to='devices.smartthermostatmodel')),
            ],
            options={
                'verbose_name': 'Thermostat subscriber',
                'verbose_name_plural': 'Thermostat subscribers',
                'ordering': ['-updated_at'],
            },
        ),
    ]
