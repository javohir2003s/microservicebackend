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



class Telegram_Users(models.Model):
    telegram_id= models.CharField(max_length=8, primary_key=True, editable=False, unique=True)
    first_name = models.CharField(max_length=150, null=True, blank=True)
    last_name = models.CharField(max_length=150, null=True, blank=True)
    phone_number = models.CharField(max_length=13, unique=True)
    username = models.CharField(max_length=20, unique=True, null=True, blank=True)
    photo = models.ImageField()


    class Meta:
        managed = False  
        db_table = 'users'  
        app_label = 'api'
