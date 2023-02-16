# Generated by Django 3.2.8 on 2021-10-12 12:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('devices', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ApartmentModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=120)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Apartment',
                'verbose_name_plural': 'Apartments',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='BoilerRoomModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=120)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Boiler room',
                'verbose_name_plural': 'Boiler rooms',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='BuildingModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=120)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Building',
                'verbose_name_plural': 'Buildings',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='ZipCodeModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('zip_code', models.CharField(default='', max_length=12)),
                ('lat_coord', models.DecimalField(blank=True, decimal_places=4, help_text='Approx. latitude coordinate of the property: 39.7456', max_digits=8, null=True)),
                ('lon_coord', models.DecimalField(blank=True, decimal_places=4, help_text='Approx. longitude coordinate of the property: -97.0892', max_digits=8, null=True)),
                ('todays_temp', models.IntegerField(blank=True, help_text='Temperature forecast for today in F', null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='ZoneModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=120)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('connection_type', models.CharField(choices=[('TST', 'Test')], default='', help_text='Connection type which was set for this zone', max_length=3)),
                ('logo', models.ImageField(blank=True, null=True, upload_to='')),
                ('controller', models.ForeignKey(blank=True, help_text='Related controller', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='zones', related_query_name='zone', to='devices.ioniqcontrollermodel')),
            ],
            options={
                'verbose_name': 'Heating zone',
                'verbose_name_plural': 'Heating zones',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='RoomModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=120)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('apartment', models.ForeignKey(help_text='The apartment this room is a part of', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='rooms', related_query_name='room', to='properties.apartmentmodel')),
                ('thermostat', models.ForeignKey(blank=True, help_text='Dedicated smart thermostat', null=True, on_delete=django.db.models.deletion.SET_NULL, to='devices.smartthermostatmodel')),
            ],
            options={
                'verbose_name': 'Rooom',
                'verbose_name_plural': 'Rooms',
                'ordering': ['-created_at'],
            },
        ),
    ]
