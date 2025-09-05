from django.db import models
from django.contrib.auth.models import User

class Person(models.Model):
    name = models.CharField(max_length=200)
    biography = models.TextField(blank=True, null=True)
    birth_date = models.DateField(null=True, blank=True)
    role = models.CharField(max_length=50, choices=[("actor", "Актёр"), ("director", "Режиссёр")])
    photo = models.ImageField(upload_to='person_photos/', blank=True, null=True)

class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Movie(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    year = models.PositiveIntegerField()
    genre = models.ManyToManyField(Genre, related_name="movies")
    poster = models.ImageField(upload_to="posters/", blank=True, null=True)
    trailer_url = models.URLField(blank=True, null=True)
    people = models.ManyToManyField(Person, related_name="movies")

    def str(self):
        return self.title

    def average_rating(self):
        return self.reviews.aggregate(models.Avg("rating"))["rating__avg"] or 0

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

class News(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='news_images/', null=True, blank=True)

class Contact(models.Model):
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    message = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.email}"