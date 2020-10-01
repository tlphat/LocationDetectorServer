"""myproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from myapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # url(r'^$', views.home, name='home'),
    # url(r'^add', views.add, name='home'),
    path('features', views.get_features, name='features'),
    path('images', views.images_handler, name='images'),
    path('images/<int:id>', views.images_detail, name='images_detail'),
    path('admin/', admin.site.urls),
    path('get_location_json', myapp_views.retrieve_location_json, name='get_location_json')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)