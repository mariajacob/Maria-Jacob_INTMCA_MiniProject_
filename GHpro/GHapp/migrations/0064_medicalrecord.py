# Generated by Django 4.2.4 on 2023-09-25 16:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('GHapp', '0063_alter_patientprofile_birth_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='MedicalRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('doctor_notes', models.TextField()),
                ('medications_needed', models.TextField()),
                ('treatments', models.TextField()),
                ('current_conditions', models.TextField()),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='GHapp.patientprofile')),
            ],
        ),
    ]