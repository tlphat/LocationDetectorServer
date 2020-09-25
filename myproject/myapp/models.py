from django.db import models

class ImageAndroid(models.Model): 
    image = models.ImageField(upload_to='images/')