# Generated by Django 3.2.9 on 2021-11-10 17:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('support', '0003_rename_supportreuquestmodel_supportrequestmodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='supportrequestmodel',
            name='email',
            field=models.EmailField(max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='supportrequestmodel',
            name='request',
            field=models.TextField(blank=True, default=''),
        ),
    ]
