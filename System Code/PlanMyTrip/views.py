from django.shortcuts import render
from Service_Scripts.PlanMyTrip_main import plan_my_trip
from Service_Scripts.Async import Plan_My_trip

# Create your views here.


def PlanMyTrip(request, *args, **kwargs):

    username = request.user.username
    email = request.user.email

    print(username,email)

    Plan_My_trip.delay(username,email)

    return render(request, 'Plan_my_trip_submitted.html', {})







