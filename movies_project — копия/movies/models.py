from django.db import models

class Movie(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=255)
    year = models.IntegerField()
    director = models.CharField(max_length=255)
    length = models.DurationField()
    rating = models.DecimalField(max_digits=3, decimal_places=1)

    def __str__(self):
        return self.title