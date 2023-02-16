# Generated by Django 3.2.8 on 2021-10-22 11:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0011_analoguethermostatmodel_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='analoguethermostatmodel',
            name='status',
            field=models.CharField(choices=[('ON', 'ON'), ('OFF', 'OFF')], default='ON', max_length=3),
        ),
    ]
