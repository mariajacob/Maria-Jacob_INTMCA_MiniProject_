# Generated by Django 4.2.4 on 2023-09-14 05:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GHapp', '0022_appointment_is_active'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appointment',
            name='is_active',
        ),
        migrations.AddField(
            model_name='ashaworker',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='preferred_time',
            field=models.TimeField(blank=True, choices=[('09:00 AM', '09:00 AM'), ('10:00 AM', '10:00 AM'), ('11:00 AM', '11:00 AM'), ('12:00 PM', '12:00 PM'), ('01:00 PM', '01:00 PM')], max_length=20, null=True),
        ),
    ]
