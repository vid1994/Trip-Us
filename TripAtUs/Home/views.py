"""
from django.shortcuts import render, redirect
from .forms import PlacesToVisitForm

# Create your views here.

def placesToVisit(request, *args, **kwargs):
    if request.method == "GET":
        form = PlacesToVisitForm()
    
    return render(request, "home.html", {'form': form})
"""