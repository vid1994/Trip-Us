# -*- coding: utf-8 -*-
"""
Created on Sat Apr 11 23:29:17 2020

@author: vidis
"""

import geocoder
from .LocationOptimizer import SearchSpace, NodeOptimizer
import numpy as np
import pandas as pd
from math import radians, cos, sin, asin, sqrt
from pymongo import MongoClient
import dns
import os

querydict = {'csrfmiddlewaretoken': ['sB3Epv7sTssiWe57L3OUeE3yJJzLwgWVlbKjBiTNQTK07127WlZR7AaG5D5LrD0h'], 'Location1': ['afadsf'], 'Preference1': ['adsfa'], 'Location2': ['asdf'], 'Preference2': ['asdfasdf'], 'Location3': ['asfdasd'], 'Preference3': ['fasdfas'], 'Location4': ['dfsdfsadf'], 'Preference4': ['asdfasdf'], 'Location5': ['asdfsd'], 'Preference5': ['fasdfsa'], 'Location6': ['fsdafsd'], 'Preference6': ['fsafdsf'], 'Rating': ['fsdfas'], 'HotelPrice': ['asdf']}
Location = querydict['Location1'][0]


def getLatnLon(LocationList):
    Latitude1 = []
    Longitude1 = []
    for location in LocationList:
        eachlocation = geocoder.osm(location)
        Latitude1.append(eachlocation.lat)
        Longitude1.append(eachlocation.lng)
        
    return Latitude1, Longitude1


scoreList = []
def BookHotel(request, username):
    
    print(request)
    
    Mongourl = "mongodb+srv://vidish:tripatus@cluster0-jzyrn.mongodb.net/test"
    
    client = MongoClient(Mongourl)
    
    d = dict((db, [collection for collection in client[db].collection_names()])
        for db in client.database_names())

    print(d)

    db = client.TravelPlan
    
    collection = db.PlacesToVisit
    
    print(username)
    
    for document in collection.find({'username':username}):
        doc = document
    
    latitude = doc['Latitude']
    longitude = doc['Longitude']
    
    search_space = SearchSpace(Latitudes=latitude, Longitudes=longitude)
    rectangular_search_space, latStepSize, lngStepSize = search_space.rectangleSearchSpace()
    lng, lat = search_space.rectangleZoneDefinition(rectangular_search_space, latStepSize, lngStepSize)
    lat = lat.tolist()
    lng = lng.tolist()
    i = 0
    while i < len(lng):
        if i + 1 != lngStepSize:
            a = 0
            while a < len(lat):
                if a + 1 != latStepSize:
                    nodeZone = [(lat[a], lng[i]),
                                (lat[a+1], lng[i]),
                                (lat[a+1], lng[i+1]),
                                (lat[a], lng[i+1])]
                    
                    node = NodeOptimizer(nodeZone)
                    centroidLat, centroidLng = node.centroidZone()
                    Distance_list = node.distanceCalculator(centroidLat, centroidLng, latitude, longitude)
                    nodeScore = node.ScoringMechanism(Distance_list)
                    scoreList.append([nodeScore, centroidLat, centroidLng])
                else:
                    pass
                a = a + 1
        else:
            pass
        i = i + 1
    
    scoreDf = scoreEvaluator(scoreList)
    Hotel_df = searchHotel(request, scoreDf)
    print(Hotel_df)
    
    hotel_dict = {"Hotel": Hotel_df['Hotel'].tolist(),
                  "Hotel_Latitude": Hotel_df['Latitude'].tolist(),
                  "Hotel_Longitude":Hotel_df['Longitude'].tolist()}
    
    print(hotel_dict)
    
    collection.update_one({'username':username},{'$set': hotel_dict}, upsert=True)
    
    print("Collection Updated")

    return Hotel_df
    
def scoreEvaluator(scoreList):
    scoreDf = pd.DataFrame()
    scoreDf['NodeScore'] = [element[0] for element in scoreList]
    scoreDf['Latitudes'] = [element[1] for element in scoreList]
    scoreDf['Longitudes'] = [element[2] for element in scoreList]
    scoreDf1 = scoreDf.drop_duplicates()
    scoreDf1 = scoreDf1[scoreDf1.NodeScore == scoreDf1.NodeScore.min()]
    return scoreDf1
#%%

def Hotel_Extraction():
    
    Mongourl = "mongodb+srv://vidish:tripatus@cluster0-jzyrn.mongodb.net/test"
    
    client = MongoClient(Mongourl)
    
    db = client.TravelPlan
    
    collection = db.HotelDB
    
    hotelDB = pd.DataFrame()
    
    hotel = []
    price = []
    rating = []
    latitude = []
    longitude = []
    img = []
    
    for document in collection.find():
        hotel.append(document['Name'])
        rating.append(document['Rating'])
        price.append(document['Price'])
        latitude.append(document['X'])
        longitude.append(document['Y'])
        img.append(document['Image'])
        
    hotelDB['Hotel'] = hotel
    hotelDB['Price'] = price
    hotelDB['Rating'] = rating
    hotelDB['Latitude'] = latitude
    hotelDB['Longitude'] = longitude
    hotelDB['Image'] = img
        
    hotelDB.replace("", np.nan, inplace=True)
    
    hotelDB = hotelDB.dropna()
    
    return hotelDB



def searchHotel(request, scoreDf):
    
    hotelsDF = Hotel_Extraction()
    hotelsDF[['Price']] = hotelsDF[['Price']].apply(pd.to_numeric)
    hotelsDF[['Rating']] = hotelsDF[['Rating']].apply(pd.to_numeric)
    
    max_price = float(request['Maximum_Price'])
    rating = float(request['Minimum_Rating'])
    
    print(max_price, rating)
    
    
    nodeLatitude = scoreDf['Latitudes']
    nodeLongitude = scoreDf['Longitudes']
    
    print(nodeLatitude, nodeLongitude)
    
    Filtered_df = hotelsDF[hotelsDF['Price'] <= max_price]
    Filtered_df = hotelsDF[hotelsDF['Rating'] >= rating]
    
    print(Filtered_df)
    
    Result_df = pd.DataFrame()
    hotel = []
    hotel_lat = []
    hotel_lng = []
    Distance_list = []
    img = []
    
    if not Filtered_df.empty:
        for index, rows in Filtered_df.iterrows():
            hotel.append(rows['Hotel'])
            distance = distanceCalculator(nodeLatitude, nodeLongitude, float(rows['Latitude']), float(rows['Longitude']))
            Distance_list.append(distance)
            hotel_lat.append(rows['Latitude'])
            hotel_lng.append(rows['Longitude'])
            img.append(rows['Image'])
            
    Result_df['Hotel'] = hotel
    Result_df['Distance'] = Distance_list
    Result_df['Latitude'] = hotel_lat
    Result_df['Longitude'] = hotel_lng
    Result_df['Image'] = img
    
    print(Result_df)
    
    Result_df = Result_df[Result_df.Distance == Result_df.Distance.min()]
    
    return Result_df
            
            
#%%
            
def distanceCalculator(centroidLat, centroidLng, Latitude1, Longitude1):
    """
    Distance is calculated between two points using radians traversed along the 
    radius of the earth. 

    Radius of Earth in km is 6371 km
    """        
    lon1, lat1, lon2, lat2 = map(radians, [centroidLng, centroidLat, Longitude1, Latitude1])

    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    
    distance = 6371* c
            
    return distance
#%%


    
    
