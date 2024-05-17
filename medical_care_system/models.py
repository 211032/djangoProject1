from django.db import models


class Employee(models.Model):
    empid = models.CharField(max_length=8, primary_key=True)
    empfname = models.CharField(max_length=64)
    emplname = models.CharField(max_length=64)
    emppasswd = models.CharField(max_length=256)
    emprole = models.IntegerField()

