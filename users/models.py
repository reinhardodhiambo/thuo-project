from django.db import models

# Create your models here.
from general.models import Counties, SubCounty


class Users(models.Model):
    fullname = models.CharField(max_length=50)
    gender = models.CharField(max_length=50)
    dob = models.DateField()
    occupation = models.CharField(max_length=50)
    mobile = models.IntegerField()
    email = models.EmailField(max_length=30)
    pin = models.CharField(max_length=50)
    national_id = models.IntegerField(primary_key=True)
    nationality = models.CharField(max_length=50)
    physical_address = models.CharField(max_length=50)
    box = models.IntegerField()
    code = models.IntegerField()
    town = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    status = models.CharField(max_length=20, default='active')

    class Meta:
        db_table = 'Users'



