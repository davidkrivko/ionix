# Generated by Django 3.2.8 on 2021-10-25 21:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_alter_tenantprofilemodel_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='tenantprofilemodel',
            name='password_reset_needed',
            field=models.BooleanField(default=False),
        ),
    ]
