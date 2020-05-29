from django.db import models


class Time(models.Model):
    active = models.BooleanField(default=True)
    start = models.DateTimeField(blank=True)
    stop = models.DateTimeField(blank=True)
