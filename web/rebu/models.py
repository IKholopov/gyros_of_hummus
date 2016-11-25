from django.db import models

class MapLayer(models.Model):
    title = models.CharField(max_length=128, blank=False)
    field = models.TextField(blank=False)
    floor = models.IntegerField(blank=False)
    a_align_x = models.FloatField(blank=False)
    a_align_y = models.FloatField(blank=False)
    b_align_x = models.FloatField(blank=False)
    b_align_y = models.FloatField(blank=False)


class Station(models.Model):
    x_coord = models.FloatField(blank=False)
    y_coord = models.FloatField(blank=False)
    floor = models.IntegerField(blank=False)