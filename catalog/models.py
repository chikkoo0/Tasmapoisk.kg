from django.db import models

class Movie(models.Model):
    title = models.CharField(max_length=100)
    poster_url = models.URLField()
    rating = models.FloatField()

    def __str__(self):
        return self.title
