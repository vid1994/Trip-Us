from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from Home.forms import PlacesToVisitForm
from Book_Hotel.forms import hotelRequirementsForm
from Service_Scripts.LocationVisitLP import placesToVisit
from django.http import HttpResponse
import urllib
from pymongo import MongoClient
from Service_Scripts.BaseMapPltCds import df_to_geojson, LocationExtraction
from PlanMyTrip.views import async_task
import dns
import json

################################
## PREFERNCES VIEW |USER FORM ##
################################


def my_view(request):
    username = None
    if request.user.is_authenticated():
        username = request.user.username
    return username

@login_required
def home(request, *args, **kwargs):
    if request.method == "GET":
        form = PlacesToVisitForm()
    else:
        print("Atleast it is coming here!")
        form = PlacesToVisitForm(request.POST)
        print(form.data)
        if form.is_valid():
            #try:
            travellingWith = form.data['Travelling_With']
            preferenceList = [form.data['Culture_Architectural'], form.data['Sight_Seeing'], form.data['Natural'],
            form.data['Shopping'], form.data['Outdoor'], form.data['Fun_Things_To_Do']]
            preferenceList = [float(x) for x in preferenceList]
            timeSpent = float(form.data['Time_Spent_Days'])
            username = request.user.username

            print(travellingWith, preferenceList, timeSpent, username)

            location, description, img = placesToVisit(travellingWith,preferenceList,timeSpent,username)
            Location_list = zip(location, description, img)
            context={
                "Locations": Location_list,
                }
            
            #except:
                ## Remeber to raise an exception msg here
            #    form = PlacesToVisitForm()
            #    return render(request, 'home.html', {'form': form})
            
            return render(request, "PlacesToVisit.html", context)

        
        form = PlacesToVisitForm()

    return render(request, 'home.html', {'form':form})


def locationPlotter(request, *args, **kwargs):
    username = request.user.username
    df = LocationExtraction(username)
    cols = ['name']
    LocationJson = df_to_geojson(df,cols)
    LocationJson = json.dumps(LocationJson)
    print(LocationJson)
    
    return HttpResponse(LocationJson, content_type='json')
