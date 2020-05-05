from django.shortcuts import render
from .forms import FeedbackForm
from Service_Scripts.FeedBackSave import Feedback_to_db

# Create your views here.

def FeedbackView(request, *args, **kwargs):
    if request.method == "GET":
        form = FeedbackForm()
    else:
        form  = FeedbackForm(request.POST)
        data = form.data
        print(data)
        username = request.user.username
        email = request.user.email
        print(username, email)
        if form.is_valid():
            Feedback_to_db(data, username, email)

            return render (request, "Thankyou.html", {})

        else:
            form = FeedbackForm()
    
    return render(request, 'Feedback.html', {'form': form})




    