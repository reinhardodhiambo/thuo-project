from django.db import models

# Create your models here.
import uuid


class Counties(models.Model):
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    county_id = models.IntegerField(primary_key=True)
    county_name = models.CharField(max_length=50)


class SubCounty(models.Model):
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    subcounty_id = models.IntegerField(primary_key=True)
    county = models.ForeignKey(Counties, on_delete=models.CASCADE, )
    subcounty_name = models.CharField(max_length=100)
