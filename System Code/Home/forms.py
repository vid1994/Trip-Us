from django import forms
from django.forms import ModelForm
from .models import PlacesToVisit


class PlacesToVisitForm(forms.ModelForm):

    class Meta:

        model = PlacesToVisit

        fields = ['Travelling_With','Culture_Architectural','Sight_Seeing','Natural','Shopping','Outdoor','Fun_Things_To_Do','Time_Spent_Days']

    