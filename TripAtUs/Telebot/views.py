from django.shortcuts import render

# Create your views here.
def telebotview(request , *args, **kwargs):
    return render(request, 'telebot.html', {})
