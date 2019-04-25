from django.db import models

# Create your models here.
class House(models.Model):
    # Name
    name = models.CharField(max_length=10)
    lng = models.FloatField()
    lat = models.FloatField()

    # Basic
    age = models.IntegerField(blank=True)
    price = models.FloatField(blank=True)
    address = models.CharField(max_length=100, blank=True)
    type = models.CharField(max_length=100, blank=True)

    # Dynamic
    is_near_park = models.BooleanField(default=1)
