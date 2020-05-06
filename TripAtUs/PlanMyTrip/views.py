from django.shortcuts import render
from Service_Scripts.PlanMyTrip_main import plan_my_trip
from django_q.tasks import async_task
from Service_Scripts.Async import plan_my_trip

# Create your views here.


def PlanMyTrip(request, *args, **kwargs):

    username = request.user.username
    email = request.user.email

    print(username,email)

    plan_my_trip.delay(username,email)

    return render(request, 'Plan_my_trip_submitted.html', {})







