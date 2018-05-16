from django.db import models


# Create your models here.
class Counties(models.Model):
    county_id = models.IntegerField(primary_key=True)
    county_name = models.CharField(max_length=50)


class SubCounty(models.Model):
    subcounty_id = models.IntegerField(primary_key=True)
    county = models.ForeignKey(Counties, on_delete=models.CASCADE,)
    subcounty_name = models.CharField(max_length=100)
