# Generated by Django 4.2.4 on 2023-09-19 07:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GHapp', '0041_alter_patientprofile_bmi'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='email',
            field=models.EmailField(max_length=254),
        ),
    ]
