# Generated by Django 4.2.4 on 2023-09-17 17:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('GHapp', '0036_appointment'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='ashaworker',
            unique_together={('Name', 'ward')},
        ),
    ]
