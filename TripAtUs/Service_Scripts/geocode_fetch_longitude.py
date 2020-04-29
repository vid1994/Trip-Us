#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 16:56:14 2020

@author: ankeittaksh
"""
import urllib
import urllib.request
import json

gmaps_api_key = 'AIzaSyD_Ez8tC_CRaHBDVM9fLrSEAJV5JP7Vq-U'
 


test = "460 corporation road"
def geocode_fetch_longitude(address):
    geocode_base_url = 'https://maps.googleapis.com/maps/api/geocode/json'
    url = geocode_base_url + '?' + "address=" + urllib.parse.quote(address) + '&' + "key" + "=" + (gmaps_api_key)
# Test value   url = 'https://maps.googleapis.com/maps/api/geocode/json?address=460%20corporation%20road&key=AIzaSyD_Ez8tC_CRaHBDVM9fLrSEAJV5JP7Vq-U'  
#    print(url)
    jsonApicall =  urllib.request.urlopen(url)

    data = json.load(jsonApicall)

    plcLong = (data['results'][0]['geometry']['location']['lng'])

    return(plcLong)

plcLongitude = geocode_fetch_longitude(test)
print(plcLongitude)
