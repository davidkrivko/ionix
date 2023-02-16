# Generated by Django 3.2.8 on 2021-10-30 20:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0024_alter_smartthermostatmodel_set_temperature'),
    ]

    operations = [
        migrations.AddField(
            model_name='analoguethermostatmodel',
            name='make',
            field=models.CharField(blank=True, default='', max_length=60),
        ),
        migrations.AddField(
            model_name='analoguethermostatmodel',
            name='model',
            field=models.CharField(blank=True, default='', max_length=60),
        ),
        migrations.AddField(
            model_name='boilermodel',
            name='installation_date',
            field=models.DateField(null=True),
        ),
    ]
