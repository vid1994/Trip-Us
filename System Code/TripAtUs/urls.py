"""TripAtUs URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import include, url
from .views import home, locationPlotter
from accounts.views import login_view, register_view, logout_view
from Book_Hotel.views import BookHotelView
from Feedback.views import FeedbackView
from Telebot.views import telebotview
from PlanMyTrip.views import PlanMyTrip

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/login/', login_view, name='login'),
    path('accounts/register/', register_view, name='signup'),
    path('accounts/logout', logout_view, name='logout'),
    path('BookHotel', BookHotelView, name='BookHotel'),
    path('Telebot' , telebotview, name='Telebot'),
    path('', home, name='Home'),
    url(r'^location/$', locationPlotter, name='location'),
    path('Feedback', FeedbackView, name = 'Feedback'),
    url(r'^send_command$', PlanMyTrip, name='send_command')
]
