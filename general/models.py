from django.db import models

# Create your models here.
import uuid


class Counties(models.Model):
    transaction_id = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    county_id = models.IntegerField(primary_key=True)
    county_name = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True, null=True)


class SubCounty(models.Model):
    transaction_id = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    subcounty_id = models.IntegerField(primary_key=True)
    county = models.ForeignKey(Counties, on_delete=models.CASCADE, )
    subcounty_name = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True, null=True)
