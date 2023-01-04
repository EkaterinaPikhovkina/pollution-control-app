from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Sensor(models.Model):
    name = models.CharField(max_length=100, null=True, verbose_name="Назва")
    kind = models.CharField(max_length=30, null=True, verbose_name="Вид датчику")
    api_name = models.CharField(max_length=100, null=True, verbose_name="Назва для API")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Датчик'
        verbose_name_plural = 'Датчики'
        ordering = ['kind', 'name']


class Pollutant(models.Model):
    name = models.CharField(max_length=100, null=True, verbose_name="Назва")
    norm_ind = models.FloatField(null=True, verbose_name="Нормальний показник(мкг/м³)")
    api_name = models.CharField(max_length=100, null=True, verbose_name="Назва для API")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Забрудник'
        verbose_name_plural = 'Забрудники'
        ordering = ['name']


class City(models.Model):
    name = models.CharField(max_length=30, null=True, verbose_name="Назва")
    api_name = models.CharField(max_length=100, null=True, verbose_name="Назва для API")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Місто'
        verbose_name_plural = 'Міста'
        ordering = ['name']


class AirData(models.Model):
    datetime = models.DateTimeField(default=timezone.now, verbose_name="Дата та час")
    city = models.ForeignKey(City, on_delete=models.PROTECT, null=True, verbose_name="Місто")
    pollutant = models.ForeignKey(Pollutant, on_delete=models.PROTECT, null=True, verbose_name="Забрудник")
    concentration = models.FloatField(null=True, verbose_name="Концентрація(мкг/м³)")
    sensor = models.ForeignKey(Sensor, on_delete=models.PROTECT, null=True, verbose_name="Датчик")
    author = models.ForeignKey(User, on_delete=models.PROTECT, null=True, verbose_name="Автор запису")

    def __str__(self):
        return self.datetime

    class Meta:
        verbose_name = 'Дані'
        verbose_name_plural = 'Дані'
        ordering = ['id']


class Prevention(models.Model):
    description = models.TextField(blank=True, null=True, verbose_name="Опис")

    def __str__(self):
        return self.description

    class Meta:
        verbose_name = 'Попередження'
        verbose_name_plural = 'Попередження'
        ordering = ['id']


class Advice(models.Model):
    pollutant = models.ForeignKey(Pollutant, on_delete=models.PROTECT, null=True, verbose_name="Забрудник")
    prevention = models.ForeignKey(Prevention, on_delete=models.PROTECT, null=True, verbose_name="Попередження")

    def __str__(self):
        return self.prevention.description

    class Meta:
        verbose_name = 'Попередження по забруднику'
        verbose_name_plural = 'Попередження по забрудниках'
        ordering = ['pollutant']


class News(models.Model):
    datetime = models.DateTimeField(default=timezone.now, null=True, verbose_name="Дата та час публікації")
    advice = models.ForeignKey(Advice, on_delete=models.PROTECT, null=True, verbose_name="Попередження")

    def __str__(self):
        return str(self.datetime)

    class Meta:
        verbose_name = 'Новина'
        verbose_name_plural = 'Новини'
        ordering = ['datetime']
