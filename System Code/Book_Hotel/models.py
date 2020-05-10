from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator 

# Create your models here.

class hotelRequirements(models.Model):
    Minimum_Rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(7)])
    Maximum_Price = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(600)])

