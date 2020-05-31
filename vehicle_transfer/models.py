from django.db import models

# Create your models here.
from users.models import Users
from vehicle_registration.models import Vehicles, Owner
import uuid


class Details(models.Model):
    transaction_id = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    transfer_id = models.AutoField(primary_key=True)
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, )
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
    previous_owner_name = models.CharField(max_length=50)
    previous_owner_mobile = models.IntegerField()
    previous_owner_email = models.EmailField(max_length=30)
    vehicle_status = models.CharField(max_length=10,
                                      default='0')  # 0 = not accepted transfer AND 1 = accepted transfer AND 11 = transferred more than once
    previous_hash = models.CharField(max_length=100)
    hash = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        db_table = 'Vehicles_Transfered'
