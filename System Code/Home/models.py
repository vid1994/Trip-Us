from django.db import models

# Create your models here.

preferenceChoice = ( 
    ("3", "High"), 
    ("2", "Medium"), 
    ("1", "Low")
) 

travelChoice = ( 
    ("Solo", "Solo"), 
    ("Family", "Family"), 
    ("Friends", "Friends")
) 

class PlacesToVisit(models.Model):
    Travelling_With = models.CharField(max_length=90, choices=travelChoice)
    Culture_Architectural = models.CharField(max_length=90, choices=preferenceChoice)
    Sight_Seeing = models.CharField(max_length=90, choices=preferenceChoice)
    Natural = models.CharField(max_length=90, choices=preferenceChoice)
    Shopping = models.CharField(max_length=90, choices=preferenceChoice)
    Outdoor = models.CharField(max_length=90, choices=preferenceChoice)
    Fun_Things_To_Do = models.CharField(max_length=90, choices=preferenceChoice)
    Time_Spent_Days = models.IntegerField()
    Locations = models.TextField()
    Latitudes = models.TextField()
    Longitudes = models.TextField()