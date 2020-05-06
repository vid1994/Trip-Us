# -*- coding: utf-8 -*-
"""
Created on Tue Apr 21 10:41:41 2020

@author: vidish
"""

"""
Linear Programming to decide on the locations to visit

==================
Problem Definition
==================

Objective function --> Maximise the Likeability score (Likeability score is determined by
                        summation of popularity (amongst travelers) * weight assigned by traveler)


Constraints --> Time constraints from the number of days per visit [Hard constraint of 10 hours of traveling per day]

Variables --> Binary variables with stat 0 --> unvisit and state 1 --> visit


===================
FUNCTION DEFINITION
===================

Inputs --> user rating (individual on each categories)
Outputs --> location to visit --> to be fed to the Book Hotel Brute force search algorithms

"""
    
        
from pulp import *
import pulp
import os
import pandas as pd
from pymongo import MongoClient
import dns

def unique(list1):
    list2 = []
    for item in list1:
        if item not in list2:
            list2.append(item)
        else:
            pass
        
    return list2


def split(word):
    return[char for char in word]


def LocationListing(item):
    new_list = []
    for char in split(item):
        if char == "_":
            new_list.append(" ")
        else:
            new_list.append(char)
            
    new_item = "".join(new_list[2:])
    
    return new_item

def Flatten(list1):
    list2 = []
    for sublist in list1:
        for item in sublist:
            list2.append(item)
            
    return list2

def placesToVisit(travellingWith, preferenceList, timeSpent, username):
    
    Mongourl = "mongodb+srv://vidish:tripatus@cluster0-jzyrn.mongodb.net/test"
    
    client = MongoClient(Mongourl)
    
    d = dict((db, [collection for collection in client[db].collection_names()])
        for db in client.database_names())

    db = client.TravelPlan
    
    collection = db.AttractionDB
    
    for doc in collection.find():
        document = doc
    
    return document
    
    print("-------------CONNECTION SUCCESSFUL----------------------")
    
    Attractions = []
    Categories = []
    Likeability_Solo = []
    Likeability_Family = []
    Likeability_Friends = []
    Time_Spent = []
    Latitude = []
    Longitude = []
    Description = []
    Image_Path = []
        
    
    for doc in collection.find():
        Attractions.append(doc['PAGETITLE'])
        Categories.append(doc['Leaf Node Category'])
        Likeability_Solo.append(doc['Likeability Solo'])
        Likeability_Family.append(doc['Likeability Family'])
        Likeability_Friends.append(doc['Likeability Friends'])
        Time_Spent.append(doc['Hour'])
        Latitude.append(doc['Latitude'])
        Longitude.append(doc['Longitude'])
        Description.append(doc['Description'])
        Image_Path.append(doc['Image Path'])
    # os.chdir("C:/Users/vidis/OneDrive/Desktop")
    
    # Attraction_Df = pd.read_excel("AttractionDB (Clean with Full Data) 27th April 2204.xlsx", sheet_name = 'Sheet1')
    
    Likeability_Df = pd.DataFrame()
    
    Likeability_Df['Attractions'] = Attractions
    Likeability_Df['Attraction Category'] = Categories
    Likeability_Df['Popularity (solo)'] = [float(x) for x in Likeability_Solo]
    Likeability_Df['Popularity (Family)'] = [float(x) for x in Likeability_Family]
    Likeability_Df['Popularity (Friends)'] = [float(x) for x in Likeability_Friends]
    Likeability_Df['Time Spent'] = [float(x) for x in Time_Spent]
    Likeability_Df['Latitude'] = [float(x) for x in Latitude]
    Likeability_Df['Longitude'] = [float(x) for x in Longitude]
    Likeability_Df['Description'] = Description
    Likeability_Df['Image Path'] = Image_Path
    
    print(Likeability_Df.shape)
    
    preferenceWeights = []
    for index, rows in Likeability_Df.iterrows():
        if rows['Attraction Category'] == "Cultural & Architecture":
            preferenceWeights.append(preferenceList[0])
        elif rows['Attraction Category'] == "Sight Seeing":
            preferenceWeights.append(preferenceList[1])
        elif rows['Attraction Category'] == "Nature":
            preferenceWeights.append(preferenceList[2])
        elif rows['Attraction Category'] == "Shopping":
            preferenceWeights.append(preferenceList[3])
        elif rows['Attraction Category'] == "Outdoor":
            preferenceWeights.append(preferenceList[4])
        elif rows['Attraction Category'] == "Fun-Things-To-Do":
            preferenceWeights.append(preferenceList[5])

            
    print(len(preferenceWeights))
    Likeability_Df['Preference Weights'] = preferenceWeights
            
        
    problem = LpProblem("LocationDecider", LpMaximize)


    x = pulp.LpVariable.dicts( "x", indexs = Likeability_Df['Attractions'].tolist(), lowBound=0, upBound=1, cat='Integer', indexStart=[] )

    if travellingWith == 'Solo':
        Likeability_Df['Preference Solo'] = [x*y for x,y in zip(Likeability_Df['Popularity (solo)'],Likeability_Df['Preference Weights'])]
        Popularity = dict(zip(Likeability_Df['Attractions'].tolist(), Likeability_Df['Preference Solo'].tolist()))
        Time = dict(zip(Likeability_Df['Attractions'].tolist(), Likeability_Df['Time Spent'].tolist()))
    elif travellingWith == 'Family':
        Likeability_Df['Preference Family'] = [x*y for x,y in zip(Likeability_Df['Popularity (Family)'],Likeability_Df['Preference Weights'])]
        Popularity = dict(zip(Likeability_Df['Attractions'].tolist(), Likeability_Df['Preference Family'].tolist()))
        Time = dict(zip(Likeability_Df['Attractions'].tolist(), Likeability_Df['Time Spent'].tolist()))
    elif travellingWith == "Friends":
        Likeability_Df['Preference Friends'] = [x*y for x,y in zip(Likeability_Df['Popularity (Friends)'],Likeability_Df['Preference Weights'])]
        Popularity = dict(zip(Likeability_Df['Attractions'].tolist(), Likeability_Df['Popularity (Friends)'].tolist()))
        Time = dict(zip(Likeability_Df['Attractions'].tolist(), Likeability_Df['Time Spent'].tolist()))
        
    
    problem += pulp.lpSum([x[i]*Popularity[i] for i in Likeability_Df['Attractions'].tolist()])
    
    
    problem += pulp.lpSum([x[i]*Time[i] for i in Likeability_Df['Attractions'].tolist()]) <= (timeSpent*10)
        
    problem.solve()
    
#    descriptions = []
#    
#    for place in v.varValue:  
#        placeDescription = Likeability_Df[Likeability_Df['Attractions'] == place]['']
#        descriptions.append(placeDescription)
    location = []
    
    for v in problem.variables():
        if v.varValue == 1:
            location.append(LocationListing(v.name))
    
    latitude = []
    longitude = []
    description = []
    img_src = []
    
    for place in location:
        temp_df = Likeability_Df[Likeability_Df['Attractions'] == place]
        latitude.append(temp_df['Latitude'].tolist())
        longitude.append(temp_df['Longitude'].tolist())
        description.append(temp_df['Description'].tolist())        
        img_src.append(temp_df['Image Path'].tolist())
    
    
    
    latitude = Flatten(latitude)
    longitude = Flatten(longitude)
    description = Flatten(description)
    img_src = Flatten(img_src)
    print(img_src)
    
    location_dict = {"Locations": location,
                 "Latitude": latitude,
                 "Longitude": longitude,
                 "Duration of trip": timeSpent,
                 "User_Preferences": preferenceWeights}
    
    collection = db.PlacesToVisit

    collection.update_one({'username':username},{'$set': location_dict}, upsert=True)
            
    return location, description, img_src
    

locations = placesToVisit(travellingWith="Family", preferenceList=[1,3,2,1,2,1],timeSpent=3,username='mark')
