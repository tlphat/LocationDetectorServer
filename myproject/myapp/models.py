from django.db import models
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFit

thumbnail_size = 200

class ImageNode(models.Model): 
    image = models.ImageField(upload_to='images/')
    thumbnail = ImageSpecField(source='image', 
                                processors=[ResizeToFit(width=thumbnail_size, height=thumbnail_size)], 
                                format='JPEG', 
                                options={'quality': 60})
    date_uploaded = models.DateTimeField(auto_now_add=True)
    angle = models.CharField(max_length=30, default=242)
    longitude = models.CharField(max_length=30, default=242)
    latitude = models.CharField(max_length=30, default=242)

class ServerInfo(models.Model):
    version = models.CharField(max_length=20)
    