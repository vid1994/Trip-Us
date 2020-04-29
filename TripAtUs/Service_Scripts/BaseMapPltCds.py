# -*- coding: utf-8 -*-
"""
Created on Sun Mar 22 07:42:53 2020

@author: vidis
"""

"""
Need to find the coordinates for Singapore - could not find as of yet from the internet

Please install basemap whl file https://www.lfd.uci.edu/~gohlke/pythonlibs/

"""


"""
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np

m = Basemap(projection = 'mill',
            llcrnrlat = 1.1,
            llcrnrlon = 102,
            urcrnrlat = 1.5,
            urcrnrlon = 104,
            resolution = 'l')

m.drawcountries()
m.drawcoastlines()
m.drawstates()
#m.drawmapscale()
m.drawcounties()

#m.drawparallels(np.arange(-90,90,10), labels = [True,False,False,False])
#m.drawmeridians(np.arange(-180,180,30), labels = [0,0,0,1])

m.scatter(103.657,1.321,latlon=True, s = 200, c = "red", marker = '^')

    #plt.title("World BaseMap", fontsize = 20)
plt.show()


"""

"""
from ipyleaflet import Map, Marker
# install geocoder first from python.org python package index
import geocoder

# location address
location = geocoder.osm('Rivervale Primary School')

# to view location details use location.json

# latitude and longitude of location
latlng = [location.lat, location.lng]

print(location.json)

# create map
#Tanjong_Pagar_map = Map(center=latlng)
#
## marker
#marker = Marker(location=latlng, title='197 Rivervale Drive')
#Tanjong_Pagar_map.add_layer(marker)
#
## display map
#Tanjong_Pagar_map
"""


import pandas as pd
from pymongo import MongoClient



def df_to_geojson(df, properties, lat='lat', lon='long'):

    geojson = {'type':'FeatureCollection', 'features':[]}
    for _, row in df.iterrows():
        feature = {'type':'Feature',
                   'properties':{},
                   'geometry':{'type':'Point','coordinates':[]}}
        feature['geometry']['coordinates'] = [row[lon],row[lat]]
        for prop in properties:
            feature['properties'][prop] = row[prop]
        geojson['features'].append(feature)
    return geojson

def LocationExtraction(username):
    
    Mongourl = "mongodb+srv://vidish:tripatus@cluster0-jzyrn.mongodb.net/test"
    
    client = MongoClient(Mongourl)
    
    db = client.TravelPlan

    collection = db.PlacesToVisit
    
    df = pd.DataFrame()
    
    for doc in collection.find({'username':username}):
        Latitude = doc['Latitude']
        Longitude = doc['Longitude']
        name = doc['Locations']
        Hotel = doc['Hotel'][0]
        Hotel_Latitude = doc['Hotel_Latitude'][0]
        Hotel_Longitude = doc['Hotel_Longitude'][0]
        
    Latitude.append(Hotel_Latitude)
    Longitude.append(Hotel_Longitude)
    name.append(Hotel)
    
    df['lat'] = Latitude
    df['long'] = Longitude
    df['name'] = name
    
    return df
