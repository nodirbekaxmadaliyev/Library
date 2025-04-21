from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import date
# Create your models here.
class Book(models.Model):
    book_id = models.PositiveIntegerField(unique=True, blank=True)
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

    def save(self, *args, **kwargs):
        if not self.book_id:
            existing_book_ids = set(Book.objects.values_list('book_id', flat=True))
            i = 1
            while i in existing_book_ids:
                i += 1
            self.book_id = i
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name