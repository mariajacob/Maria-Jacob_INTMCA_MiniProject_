# Generated by Django 4.2.4 on 2023-09-13 03:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GHapp', '0017_ashaworker_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='ashaworker',
            name='password',
            field=models.CharField(blank=True, max_length=100, null=True, unique=True),
        ),
    ]
