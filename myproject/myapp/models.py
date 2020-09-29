from django.db import models

class ImageNode(models.Model): 
    image = models.ImageField(upload_to='images/')
    angle = models.CharField(max_length=30, default=242)
    longitude = models.CharField(max_length=30, default=242)
    latitude = models.CharField(max_length=30, default=242)

class ServerInfo(models.Model):
    version = models.CharField(max_length=20)
    