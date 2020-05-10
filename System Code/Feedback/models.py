from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator 

Choices = ( 
    ("Excellent", "Excellent"), 
    ("Very Good", "Very Good"), 
    ("Good", "Good"),
    ("Neutral", "Neutral"),
    ("Bad", "Bad"),
    ("Very Bad", "Very Bad"),
    ("Horrible", "Horrible"),
) 

# Create your models here.

class Feedback(models.Model):
    ServiceRating = models.CharField(max_length=90, choices=Choices)
    ServiceFeedback = models.TextField()
    
