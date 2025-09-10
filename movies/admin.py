from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from .models import Movie, Review, Genre, Contact, Person, Favorite, News

class MediaMixin(TranslationAdmin):
    class Media:
        js = (
            "https://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js",
            "https://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js",
            "modeltranslation/js/tabbed_translation_fields.js",
            "adminsortable2/js/plugins/admincompat.js",
            "adminsortable2/js/libs/jquery.ui.core-1.11.4.js",
            "adminsortable2/js/libs/jquery.ui.widget-1.11.4.js",
            "adminsortable2/js/libs/jquery.ui.mouse-1.11.4.js",
            "adminsortable2/js/libs/jquery.ui.touch-punch-0.2.3.js",
            "adminsortable2/js/libs/jquery.ui.sortable-1.11.4.js",
        )
        css = {
            "screen": ("modeltranslation/css/tabbed_translation_fields.css",),
        }

@admin.register(Movie)
class MovieAdmin(MediaMixin):
    list_display = ('title',)

admin.site.register(Review)
admin.site.register(Genre)
admin.site.register(Contact)
admin.site.register(Person)
admin.site.register(Favorite)
admin.site.register(News)




