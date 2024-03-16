# Generated by Django 4.2.4 on 2024-03-05 05:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('GHapp', '0110_medicine_medicinecategory_nurse_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='wardmem',
            field=models.IntegerField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='prescription',
            name='patient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='GHapp.patientprofile'),
        ),
    ]
