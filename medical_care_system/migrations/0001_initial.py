# Generated by Django 5.1.1 on 2024-09-20 05:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('empid', models.CharField(max_length=8, primary_key=True, serialize=False)),
                ('empfname', models.CharField(max_length=64)),
                ('emplname', models.CharField(max_length=64)),
                ('emppasswd', models.CharField(max_length=256)),
                ('emprole', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='medicine',
            fields=[
                ('medicineid', models.CharField(max_length=8, primary_key=True, serialize=False)),
                ('medicinename', models.CharField(max_length=64)),
                ('unit', models.CharField(max_length=8)),
            ],
        ),
        migrations.CreateModel(
            name='patient',
            fields=[
                ('patid', models.CharField(max_length=8, primary_key=True, serialize=False)),
                ('patfname', models.CharField(max_length=64)),
                ('patlname', models.CharField(max_length=64)),
                ('hokenmei', models.CharField(max_length=64)),
                ('hokenexp', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='shiiregyousha',
            fields=[
                ('shiireid', models.CharField(max_length=8, primary_key=True, serialize=False)),
                ('shiiremei', models.CharField(max_length=64)),
                ('shiireaddress', models.CharField(max_length=64)),
                ('shiiretel', models.CharField(max_length=64)),
                ('shiirehonkin', models.IntegerField()),
                ('nouki', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Tabyouin',
            fields=[
                ('tabyouinid', models.CharField(max_length=8, primary_key=True, serialize=False)),
                ('tabyouinmei', models.CharField(max_length=64)),
                ('tabyouinaddress', models.CharField(max_length=64)),
                ('tabyouintel', models.CharField(max_length=64)),
                ('tabyouinshihonkin', models.IntegerField()),
                ('kyukyu', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Treatment',
            fields=[
                ('treatment_id', models.AutoField(primary_key=True, serialize=False)),
                ('dosage', models.IntegerField()),
                ('status', models.CharField(default='pending', max_length=10)),
                ('taken_at', models.DateTimeField(blank=True, null=True)),
                ('remaining_dosage', models.IntegerField(default=0)),
                ('hukuyou_dosage', models.IntegerField(default=0)),
                ('empid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='medical_care_system.employee')),
                ('medicineid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='medical_care_system.medicine')),
                ('patid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='medical_care_system.patient')),
            ],
        ),
    ]
