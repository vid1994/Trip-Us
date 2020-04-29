

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 13:46:40 2020

@author: ankeittaksh
"""

import urllib
import urllib.request
import json

gmaps_api_key = 'AIzaSyD_Ez8tC_CRaHBDVM9fLrSEAJV5JP7Vq-U'
 

"""
geocoding sample
The following example requests the latitude and longitude of "1600 Amphitheatre Parkway, Mountain View, CA", and specifies that the output must be in JSON format.
https://maps.googleapis.com/maps/api/geocode/json?address=1600+Amphitheatre+Parkway,+Mountain+View,+CA&key=YOUR_API_KEY
 
distance matrix
The following example requests the distance matrix data between Washington, DC and New York City, NY, in JSON format:
https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins=Washington,DC&destinations=New+York+City,NY&key=YOUR_API_KEY
 
The following example requests the driving directions from Disneyland to Universal Studios Hollywood, in JSON format:
https://maps.googleapis.com/maps/api/directions/json?origin=Disneyland&destination=Universal+Studios+Hollywood&key=YOUR_API_KEY
 

"""
test = "460 corporation road"
def geocode_fetch_latitude(address):
    geocode_base_url = 'https://maps.googleapis.com/maps/api/geocode/json'
    url = geocode_base_url + '?' + "address=" + urllib.parse.quote(address) + '&' + "key" + "=" + (gmaps_api_key)
# Test value   url = 'https://maps.googleapis.com/maps/api/geocode/json?address=460%20corporation%20road&key=AIzaSyD_Ez8tC_CRaHBDVM9fLrSEAJV5JP7Vq-U'  
#    print(url)
    jsonApicall =  urllib.request.urlopen(url)

    data = json.load(jsonApicall)

    plcLat = (data['results'][0]['geometry']['location']['lat'])

    return data, plcLat

Raw_data, plcLatitude = geocode_fetch_latitude(test)
print(plcLatitude)


