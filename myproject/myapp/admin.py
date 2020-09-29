from django.contrib import admin

# Register your models here.
from myapp.models import ImageNode
from myapp.models import ServerInfo

admin.site.register(ImageNode)
admin.site.register(ServerInfo)