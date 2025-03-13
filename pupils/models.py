from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
# Create your models here.

class Pupil(models.Model):
    id = models.BigAutoField(primary_key = True)
    first_name = models.CharField(max_length=20, null=False, blank=False)
    last_name = models.CharField(max_length=20, null=False, blank=False)
    group = models.CharField(max_length=15, null=False, blank=False)
    course = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(8)
        ],
        null=True,
        blank=True
    )
    books = models.JSONField(blank=True, default=list)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
