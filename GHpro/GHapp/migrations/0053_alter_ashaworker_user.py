# Generated by Django 4.2.4 on 2023-09-21 12:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('GHapp', '0052_alter_ashaworker_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ashaworker',
            name='user',
            field=models.OneToOneField( on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
