from django.db import models

# Create your models here.
class Rank(models.Model):
    Alink=models.URLField(blank=False)
    Flink=models.URLField(blank=False)

