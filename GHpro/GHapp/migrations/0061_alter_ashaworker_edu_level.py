# Generated by Django 4.2.4 on 2023-09-24 05:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GHapp', '0060_ashaworker_add_certificate_ashaworker_add_training_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ashaworker',
            name='edu_level',
            field=models.CharField(blank=True, choices=[('High School', 'High School'), ('Bachelors Degree', 'Bachelors Degree'), ('Masters Degree', 'Masters Degree')], max_length=100, null=True),
        ),
    ]
