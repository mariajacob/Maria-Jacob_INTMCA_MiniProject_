# Generated by Django 4.2.4 on 2023-09-18 15:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('GHapp', '0039_alter_ashaworker_ward'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='patient',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='GHapp.patientprofile'),
        ),
        migrations.AlterField(
            model_name='patientprofile',
            name='height',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='patientprofile',
            name='house_no',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='patientprofile',
            name='phone_number',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='patientprofile',
            name='pin_code',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='patientprofile',
            name='weight',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
