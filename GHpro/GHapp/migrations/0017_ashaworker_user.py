# Generated by Django 4.2.4 on 2023-09-13 03:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('GHapp', '0016_remove_ashaworker_password'),
    ]

    operations = [
        migrations.AddField(
            model_name='ashaworker',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
