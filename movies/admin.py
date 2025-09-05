from django.contrib import admin
from .models import Movie, Review, Genre, Contact, Person, Favorite, News

admin.site.register(Movie)
admin.site.register(Review)
admin.site.register(Genre)
admin.site.register(Contact)
admin.site.register(Person)
admin.site.register(Favorite)
admin.site.register(News)

