from django.db import models

class ImageAndroid(models.Model): 
    image = models.ImageField(upload_to='images/')
    angle = models.CharField(max_length=30, default=242)
    longitude = models.CharField(max_length=30, default=242)
    latitude = models.CharField(max_length=30, default=242)