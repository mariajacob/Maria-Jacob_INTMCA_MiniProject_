# Generated by Django 4.2.4 on 2023-09-19 08:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('GHapp', '0043_rename_first_name_appointment_patient_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
    ]
