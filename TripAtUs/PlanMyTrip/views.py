from django.shortcuts import render
from Service_Scripts.PlanMyTrip_main import plan_my_trip
from django_q.tasks import async_task

# Create your views here.


def PlanMyTrip(request, *args, **kwargs):

    username = request.user.username
    email = request.user.email

    print(username,email)

    try:
        async_task("TripAtUs.Service_Scripts.plan_my_trip",username,email)
    except:
        print("System error!")

    return render(request, 'Plan_my_trip_submitted.html', {})







