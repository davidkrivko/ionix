# Generated by Django 3.2.8 on 2021-10-19 09:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0006_ioniqcontrollermodel_building'),
    ]

    operations = [
        migrations.AddField(
            model_name='ioniqcontrollermodel',
            name='model_type',
            field=models.CharField(choices=[('MX', 'Ioniq Max'), ('MN', 'Ioniq Mini')], default='', max_length=2),
        ),
    ]
