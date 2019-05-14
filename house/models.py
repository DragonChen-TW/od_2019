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

    # Pre Calculated
    stat_code = models.CharField(max_length=20, default='')
    raw_stat = models.CharField(max_length=200, default='')

    # Scores
    medical_score = models.IntegerField(default=-1)
    freeway_score = models.IntegerField(default=-1)
    mrt_score = models.IntegerField(default=-1)
    light_rail_score = models.IntegerField(default=-1)
    police_score = models.IntegerField(default=-1)
    population_score = models.IntegerField(default=-1)

    # Dynamic
    is_near_park = models.BooleanField(default=1)
