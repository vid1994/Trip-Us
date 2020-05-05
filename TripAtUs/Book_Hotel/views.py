from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .forms import hotelRequirementsForm
from Service_Scripts import Main

# Create your views here.


#########################|
## BOOK MY HOTEL VIEW  ##|
#########################|

def BookHotelView(request):
    if request.method == "GET":
        form = hotelRequirementsForm()
    else:

 #       try:
        username = request.user.username
        #print("Atleast it is coming here!") ### DEBUGGING
        form = hotelRequirementsForm(request.POST)
        print(form.data)
        
        score = Main.BookHotel(form.data, username)

        Hotel_name = score['Hotel'].tolist()
        Hotel_img = score['Image'].tolist()
        Hotel_list = zip(Hotel_name, Hotel_img)

        print(Hotel_name)
        print(Hotel_img)

        context = {"Hotel": Hotel_list}

        return render(request, 'PlanMyTrip.html', context)

#        except:
#            form = hotelRequirementsForm()

#            return render(request, 'BookMyHotel.html', {'form': form})

    return render(request, 'BookMyHotel.html', {'form': form})



