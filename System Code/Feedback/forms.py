from django import forms
from .models import Feedback


Choices = ( 
    ("Excellent", "Excellent"), 
    ("Very Good", "Very Good"), 
    ("Good", "Good"),
    ("Neutral", "Neutral"),
    ("Bad", "Bad"),
    ("Very Bad", "Very Bad"),
    ("Horrible", "Horrible"),
) 


class FeedbackForm(forms.Form):

    Service_Rating = forms.ChoiceField(label='How did you like your visit to Singapore with us?', choices=Choices)
    Service_Feedback = forms.CharField(label='Do you have any feedback for us?', widget=forms.Textarea(attrs={"rows":5, "cols":20}))