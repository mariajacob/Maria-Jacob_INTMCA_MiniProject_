# Generated by Django 4.2.4 on 2023-10-06 17:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('GHapp', '0102_alter_appointment_phone_number'),
    ]

    operations = [
        migrations.CreateModel(
            name='Hca',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hcaname', models.CharField(max_length=100)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('admin_set_password', models.CharField(blank=True, max_length=128, null=True)),
                ('date_of_join', models.CharField(max_length=100)),
                ('address', models.TextField()),
                ('taluk', models.CharField(max_length=100)),
                ('Panchayat', models.CharField(max_length=100)),
                ('postal', models.IntegerField()),
                ('phone', models.IntegerField()),
                ('profile_photo', models.ImageField(blank=True, null=True, upload_to='profile_photos/')),
                ('license_certificate', models.FileField(blank=True, null=True, upload_to='lic_cert/')),
                ('year_hca', models.IntegerField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
