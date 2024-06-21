from django.db import models


class Employee(models.Model):
    empid = models.CharField(max_length=8, primary_key=True)
    empfname = models.CharField(max_length=64)
    emplname = models.CharField(max_length=64)
    emppasswd = models.CharField(max_length=256)
    emprole = models.IntegerField()

class shiiregyousha(models.Model):
    shiireid = models.CharField(max_length=8, primary_key=True)
    shiiremei = models.CharField(max_length=64)
    shiireaddress = models.CharField(max_length=64)
    shiiretel = models.CharField(max_length=64)
    shiirehonkin = models.IntegerField()
    nouki = models.IntegerField()

class patient(models.Model):
    patid = models.CharField(max_length=8, primary_key=True)
    patfname = models.CharField(max_length=64)
    patlname = models.CharField(max_length=64)
    hokenmei = models.CharField(max_length=64)
    hokenexp = models.DateField()

class medicine(models.Model):
    medicineid = models.CharField(max_length=8, primary_key=True)
    medicinename = models.CharField(max_length=64)
    unit = models.CharField(max_length=8)

class Treatment(models.Model):
    treatment_id = models.AutoField(primary_key=True)
    empid = models.ForeignKey('Employee', on_delete=models.CASCADE)
    patid = models.ForeignKey('patient', on_delete=models.CASCADE)
    medicineid = models.ForeignKey('medicine', on_delete=models.CASCADE)
    dosage = models.IntegerField()
    status = models.CharField(max_length=10, default='pending')  # 'pending' or 'confirmed'

class Tabyouin(models.Model):
    tabyouinid = models.CharField(max_length=8, primary_key=True, )
    tabyouinmei = models.CharField(max_length=64)
    tabyouinaddress = models.CharField(max_length=64)
    tabyouintel = models.CharField(max_length=64)
    tabyouinshihonkin = models.IntegerField()
    kyukyu = models.IntegerField()
