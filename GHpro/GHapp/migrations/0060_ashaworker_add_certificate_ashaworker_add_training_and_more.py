# Generated by Django 4.2.4 on 2023-09-24 05:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GHapp', '0059_ashaworker_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='ashaworker',
            name='add_certificate',
            field=models.FileField(blank=True, null=True, upload_to='add_cert/'),
        ),
        migrations.AddField(
            model_name='ashaworker',
            name='add_training',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='ashaworker',
            name='add_training_inst',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='ashaworker',
            name='edu_certificate',
            field=models.FileField(blank=True, null=True, upload_to='edu_cert/'),
        ),
        migrations.AddField(
            model_name='ashaworker',
            name='edu_inst',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='ashaworker',
            name='edu_level',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='ashaworker',
            name='id_proof',
            field=models.FileField(blank=True, null=True, upload_to='id_proofs/'),
        ),
        migrations.AddField(
            model_name='ashaworker',
            name='year_pass_add',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='ashaworker',
            name='year_pass_edu',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
