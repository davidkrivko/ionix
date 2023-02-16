# Generated by Django 3.2.8 on 2021-10-12 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AnalogueThermostatModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('pin_num', models.SmallIntegerField(help_text='pin connection index', null=True)),
                ('status', models.CharField(blank=True, choices=[('TST', 'Test status')], default='', max_length=3)),
            ],
            options={
                'verbose_name': 'Analogue thermostat',
                'verbose_name_plural': 'Analogue thermostats',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='BoilerModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('serial_num', models.CharField(default='', max_length=60)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('type', models.CharField(choices=[('TST', 'Test type')], default='', max_length=3)),
                ('health_status', models.CharField(choices=[('TST', 'Test status')], default='', help_text="Boiler's system health status", max_length=3)),
            ],
            options={
                'verbose_name': 'Boiler',
                'verbose_name_plural': 'Boilers',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='IoniqControllerModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('serial_num', models.CharField(default='', max_length=60)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('load_type', models.CharField(choices=[('TST', 'Test type')], default='', max_length=3)),
            ],
            options={
                'verbose_name': 'Ioniq controller',
                'verbose_name_plural': 'Ioniq controllers',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='SensorModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('serial_num', models.CharField(default='', max_length=60)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('pin_num', models.SmallIntegerField(help_text='PIN number used with Controller connection', null=True)),
                ('type', models.CharField(choices=[('TST', 'Test type')], default='', max_length=3)),
            ],
            options={
                'verbose_name': 'Sensor',
                'verbose_name_plural': 'Sensors',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='SmartThermostatModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('serial_num', models.CharField(default='', max_length=60)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(blank=True, choices=[('TST', 'Test status')], default='', max_length=3)),
                ('set_temperature', models.SmallIntegerField(blank=True, help_text='Field for storing thermostat owner command set temperature value', null=True)),
            ],
            options={
                'verbose_name': 'Smart thermostat',
                'verbose_name_plural': 'Smart thermostats',
                'ordering': ['-created_at'],
            },
        ),
    ]
