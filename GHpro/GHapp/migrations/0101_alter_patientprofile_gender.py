# Generated by Django 4.2.4 on 2023-10-05 10:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GHapp', '0100_alter_appointment_gender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patientprofile',
            name='gender',
            field=models.CharField(blank=True, choices=[('Male', 'Male'), ('Female', 'Female')], max_length=10, null=True),
        ),
    ]