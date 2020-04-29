from django import forms
from .models import hotelRequirements


class hotelRequirementsForm(forms.ModelForm):

    class Meta:

        model = hotelRequirements

        fields = ['Minimum_Rating', 'Maximum_Price']

        
        