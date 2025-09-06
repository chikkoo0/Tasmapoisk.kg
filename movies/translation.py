from modeltranslation.translator import register, TranslationOptions
from .models import Movie

@register(Movie)
class MovieTranslationOptions(TranslationOptions):
    # перечисляем поля для перевода
    fields = ('title', 'description')