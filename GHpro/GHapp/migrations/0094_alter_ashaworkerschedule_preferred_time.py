# Generated by Django 4.2.4 on 2023-10-02 13:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GHapp', '0093_remove_ashaworkerschedule_end_time_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ashaworkerschedule',
            name='preferred_time',
            field=models.CharField(blank=True, choices=[('09:00 AM', '09:00-10:00 AM'), ('10:00 AM', '10:00 AM'), ('11:00 AM', '11:00 AM'), ('12:00 PM', '12:00 PM'), ('01:00 PM', '01:00 PM')], max_length=20, null=True),
        ),
    ]