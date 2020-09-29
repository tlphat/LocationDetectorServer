from django import forms 
from myapp.models import ImageNode

class AndroidForm(forms.ModelForm):

    class Meta:
        model = ImageNode
        fields = ['image', 'angle', 'longitude', 'latitude']