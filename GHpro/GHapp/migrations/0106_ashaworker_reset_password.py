# Generated by Django 4.2.4 on 2023-10-10 06:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GHapp', '0105_patientprofile_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='ashaworker',
            name='reset_password',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
    ]
