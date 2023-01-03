from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Sensor(models.Model):
    name = models.CharField(max_length=100, null=True)
    kind = models.CharField(max_length=30, null=True)

    def __str__(self):
        return self.name


class Pollutant(models.Model):
    name = models.CharField(max_length=100, null=True)
    norm_ind = models.FloatField(null=True)

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=30, null=True)

    def __str__(self):
        return self.name


class AirData(models.Model):
    datetime = models.DateTimeField(default=timezone.now)
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=True)
    pollutant = models.ForeignKey(Pollutant, on_delete=models.CASCADE, null=True)
    concentration = models.FloatField(null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE, null=True)
