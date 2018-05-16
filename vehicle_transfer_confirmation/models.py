from django.db import models

# Create your models here.
# from users.models import Users
# from vehicle_registration.models import Details
# from vehicle_transfer.models import Owner
#
#
# class Status(models.Model):
#     status_id = models.AutoField(primary_key=True)
#     transfer = models.ForeignKey(Owner)
#     fullname = models.CharField(max_length=50)
#     national = models.ForeignKey(Users)
#     mobile = models.IntegerField()
#     dob = models.DateField()
#     pin = models.CharField(max_length=50)
#     email = models.EmailField(max_length=30)
#     reg = models.ForeignKey(Details)
#     vehicle_type = models.CharField(max_length=50)
#     make = models.CharField(max_length=50)
#     vehicle_model = models.CharField(max_length=50)
#     year_of_manufacture = models.CharField(max_length=10)
#     previous_owner_name = models.CharField(max_length=50)
#     previous_owner_mobile = models.IntegerField()
#     previous_owner_email = models.EmailField(max_length=30)
