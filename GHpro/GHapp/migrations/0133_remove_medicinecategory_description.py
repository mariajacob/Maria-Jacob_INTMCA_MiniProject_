# Generated by Django 4.2.4 on 2024-03-27 10:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('GHapp', '0132_rename_ward_asha_appointment_ward'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='medicinecategory',
            name='description',
        ),
    ]
