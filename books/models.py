from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import date
# Create your models here.
class Book(models.Model):
    book_code = models.CharField(max_length=15, null=False, blank=False)
    name = models.CharField(max_length=100, null=False, blank=False, unique=True)
    authors = models.CharField(max_length=150, null=False, blank=False)
    year = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1700),
            MaxValueValidator(date.today().year)
        ],
        null=False,
        blank=False,
    )
    book_lang = models.CharField(max_length=30, null=False, blank=False)
    number = models.PositiveIntegerField(null=False, blank=False)

    def __str__(self):
        return self.name