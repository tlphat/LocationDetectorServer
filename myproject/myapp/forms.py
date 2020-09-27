from django import forms 
from myapp.models import ImageAndroid

class AndroidForm(forms.ModelForm):

    class Meta:
        model = ImageAndroid
        fields = ['image', 'angle', 'longitude', 'latitude']