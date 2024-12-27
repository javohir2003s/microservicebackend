from django.db import models
from django.utils.crypto import get_random_string

# Create your models here.

class Book(models.Model):
    title = models.CharField(max_length=150)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    photo = models.ImageField(upload_to='book_images')
    description = models.TextField()

    def __str__(self):
        return self.title

