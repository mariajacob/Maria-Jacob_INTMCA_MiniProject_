# Generated by Django 4.2.4 on 2024-03-06 16:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('GHapp', '0124_delete_prescription'),
    ]

    operations = [
        migrations.CreateModel(
            name='Prescription_model',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('morning', models.BooleanField(default=False)),
                ('noon', models.BooleanField(default=False)),
                ('evening', models.BooleanField(default=False)),
                ('date_of_prescription', models.DateField()),
                ('quantity', models.PositiveIntegerField()),
                ('duration', models.CharField(max_length=100)),
                ('dosages', models.CharField(blank=True, max_length=100, null=True)),
                ('medicine', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='GHapp.medicine')),
                ('nurses', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='GHapp.nurse')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='GHapp.patientprofile')),
            ],
        ),
    ]