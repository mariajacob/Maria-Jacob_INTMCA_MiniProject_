# Generated by Django 4.2.4 on 2024-03-06 16:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('GHapp', '0117_alter_member_wardmem_alter_prescription_evening'),
    ]

    operations = [
        migrations.AddField(
            model_name='prescription',
            name='appointment',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='GHapp.appointment'),
            preserve_default=False,
        ),
    ]
    operations = [
        migrations.AlterField(
            model_name='prescription',
            name='evening',
            field=models.BooleanField(default=False, null=True, blank=True),
        ),
    ]
    operations = [
        migrations.AlterField(
            model_name='prescription',
            name='noon',
            field=models.BooleanField(default=False, null=True, blank=True),
        ),
    ]
    operations = [
        migrations.AlterField(
            model_name='prescription',
            name='morning',
            field=models.BooleanField(default=False, null=True, blank=True),
        ),
    ]