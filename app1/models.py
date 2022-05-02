from django.db import models

# Create your models here.
class Review(models.Model):
    name = models.TextField(primary_key=True,max_length=65535)
    text = models.TextField( )
    sentiment = models.BooleanField()
