# Generated by Django 5.0.6 on 2024-06-03 03:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('medical_care_system', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='treatment',
            old_name='medicine_id',
            new_name='medicineid',
        ),
    ]
