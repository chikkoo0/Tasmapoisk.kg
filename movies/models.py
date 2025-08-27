from django.db import models
from django.contrib.auth.models import User

class Movie(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    year = models.PositiveIntegerField()
    genre = models.CharField(max_length=100)
    poster = models.ImageField(upload_to="posters/", blank=True, null=True)
    trailer_url = models.URLField(blank=True, null=True)

    def str(self):
        return self.title

class Review(models.Model):
    movie = models.ForeignKey(Movie, related_name="reviews", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    rating = models.IntegerField(default=0)  # 1–10
    created_at = models.DateTimeField(auto_now_add=True)

    def str(self):
        return f"{self.user.username} → {self.movie.title}"

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'movie')