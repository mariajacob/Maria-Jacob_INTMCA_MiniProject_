# Generated by Django 4.2.4 on 2023-09-12 18:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GHapp', '0009_alter_ashaworker_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ashaworker',
            name='password',
            field=models.CharField(blank=True, max_length=128, null=True, unique=True),
        ),
    ]
