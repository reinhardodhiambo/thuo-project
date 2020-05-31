from django.db import models

# Create your models here.
from users.models import Users
import uuid


class Vehicles(models.Model):
    transaction_id = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    reg_no = models.CharField(primary_key=True, max_length=50)
    vehicle_type = models.CharField(max_length=50)
    make = models.CharField(max_length=50)
    vehicle_model = models.CharField(max_length=50)
    year_of_manufacture = models.CharField(max_length=10)
    previous_hash = models.CharField(max_length=100, default='0')
    hash = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        db_table = 'Vehicles'


class Owner(models.Model):
    transaction_id = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    owner_id = models.AutoField(primary_key=True)
    fullname = models.CharField(max_length=50)
    national = models.ForeignKey(Users, on_delete=models.CASCADE, )
    mobile = models.IntegerField()
    dob = models.DateField()
    pin = models.CharField(max_length=50)
    email = models.EmailField(max_length=30)
    reg = models.ForeignKey(Vehicles, on_delete=models.CASCADE, )
    vehicle_type = models.CharField(max_length=50)
    make = models.CharField(max_length=50)
    vehicle_model = models.CharField(max_length=50)
    year_of_manufacture = models.CharField(max_length=10)
    vehicle_status = models.CharField(max_length=20, default='owned')
    previous_hash = models.CharField(max_length=100)
    hash = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        db_table = 'Vehicle_Owner'
