from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

class Book(models.Model):
    title = models.fields.CharField(max_length = 10000)
    author = models.fields.CharField(max_length = 10000)
    rating = models.fields.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    date = models.DateTimeField(auto_now=True)
