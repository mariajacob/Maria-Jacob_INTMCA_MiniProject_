# Generated by Django 4.2.4 on 2023-09-21 13:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('GHapp', '0053_alter_ashaworker_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ashaworker',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
