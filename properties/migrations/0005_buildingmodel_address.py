# Generated by Django 3.2.8 on 2021-10-13 11:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0004_alter_boilerroommodel_apartment'),
    ]

    operations = [
        migrations.AddField(
            model_name='buildingmodel',
            name='address',
            field=models.CharField(blank=True, default='', max_length=120),
        ),
    ]
