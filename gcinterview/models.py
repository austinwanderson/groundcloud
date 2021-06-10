from django.contrib.gis.db import models

class Company(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100,blank=True,default="")

class Driver(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100,blank=True,default="")
    company_id = models.ForeignKey(Company,models.SET_NULL,blank=True,null=True)

class Truck(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    current_location = models.PointField()
    current_driver = models.ForeignKey(Driver,models.SET_NULL,blank=True,null=True)