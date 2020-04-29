# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import math
##Below is a rough prototype on how the backend algorithm will work

#Distance_list = [12,2,6,10,2,3]
Preference_list = [4,2,2,2]


Location = [{'Suntec City': {'Latitude': 1.293494,
                            'Longitude': 103.857170},
            'Yu Hua Secondary School, Singapore': {'Latitude': 1.347026,
                                                   'Longitude': 103.724052},
            'Mustafa Shopping Center': {'Latitude': 1.3521,
                                        'Longitude': 103.8198
                    }
        }]
            

"""
Need a function that converts the above format into a list of latitudes and longitudes for each location.
Please add it over here.

"""

Latitudes1 = [1.293494, 1.347026, 1.3521]
Longitudes1 = [103.8198, 103.724052, 103.857170]


"""
Temporarily using Geocoder to obtain the latitudes and longitudes of the location
"""
#%%
import geocoder
import math
##Below is a rough prototype on how the backend algorithm will work

#Distance_list = [12,2,6,10,2,3]
Preference_list = [2,3,2,4,3,2]

location1 = "Jurong Bird Park Singapore"
location2 = "Marina Bay Sands"
location3 = "Singapore Zoo"
location4 = "Ion Orchard Singapore"
location5 = "Universal Studios Singapore"
location6 = "Changi Beach Singapore"


location = [location1, location2, location3, location4, location5, location6]

Latitude1 = []
Longitude1 = []

for eachLoc in location:
    eachlocation = geocoder.osm(eachLoc)
    Latitude1.append(eachlocation.lat)
    Longitude1.append(eachlocation.lng)

#%%
"""
======================================================
LOCATION OPTIMIZER - RENT@US BACKEND CODE DEVELOPEMENT
======================================================
Node: A node represents the smallest user-defined divisible area of the search space

Each node will require the following functions to work
1) Initialization
    - boundary conditions of the node - boundary latitude & longitude (in cartesian planes x & y)
    - Location preference in terms of latitude & longitude (in cartesian planes x & y - cached locations)
    - User preferences as defined at the front-end
    
2) Distance API calculator

3) Scoring Mechanism 


"""

import numpy as np
import pandas as pd
from math import radians, cos, sin, asin, sqrt


class SearchSpace:
    
    """
    Initialization of the loaction information
    """
    
    def __init__(self, Latitudes, Longitudes):
        self.Latitudes = Latitudes
        self.Longitudes = Longitudes

    """
    Search Space computation - Conversion into a square search space
    
    Advantages
    ----------
    
    1) Easy to compute the search space
    
    Disadvantages
    -------------
    
    1) Square search space leads to exploration of suboptimal solution depending on 
    user location preferences
    
    |--------------|
    |    .A        |
    |              |
    |       .B     |
    |              |
    |      .C      |
    |--------------|
    
    Search space becomes magnified as seen because vertical distance from A to C far outruns
    the horizontal span.
    
    Hence, may not be the most effective
    
    """
   
    def squareSearchSpace (self):
        rangeLatitude = max(self.Latitudes) - min(self.Latitudes)
        rangeLongitude = max(self.Longitudes) - min(self.Longitudes)
        sideSquare = max(rangeLatitude, rangeLongitude)
        
        """
        side square provides us with the side of each square, next is to find the 4 vertices of
        the coordinates
        """
        
        verticeA = (min(self.Latitudes), min(self.Longitudes))
        verticeB = (min(self.Latitudes)+sideSquare, min(self.Longitudes))
        verticeC = (min(self.Latitudes)+sideSquare, min(self.Longitudes)+sideSquare)
        verticeD = (min(self.Latitudes),min(self.Longitudes)+sideSquare)
        
        searchSpace = [verticeA, verticeB, verticeC, verticeD]
        
        stepSize = math.floor(sideSquare/0.001)
        
        return searchSpace, stepSize
    
    def rectangleSearchSpace(self):
        rangeLatitude = max(self.Latitudes) - min(self.Latitudes)
        rangeLonigtude = max(self.Longitudes) - min(self.Longitudes)
        sideA = rangeLatitude
        sideB = rangeLonigtude
        
        """
        rectangle search space provides us two sides: length and the breadth. Next job is to find
        the 4 vertices of the rectangle.
        
        The rectangle search space avoids the suboptimal space exploration that square search space
        results in. 
        
        """
        
        verticeA = (min(self.Latitudes),min(self.Longitudes))
        verticeB = (min(self.Latitudes),min(self.Longitudes)+sideB)
        verticeC = (min(self.Latitudes)+sideA, min(self.Longitudes))
        verticeD = (min(self.Latitudes)+sideA, min(self.Longitudes)+sideB)
        
        latStepSize = math.floor(sideA/0.01)
        lngStepSize = math.floor(sideB/0.01)        
        
        searchSpace = [verticeA, verticeB, verticeC, verticeD]
        
        return searchSpace, latStepSize, lngStepSize
        
        
    def squareZoneDefinition(self, searchSpace, ngrid):
        
        """
        ngrid is the number of grids required in the search space
        """
        bottomLeft = searchSpace[0]
        bottomRight = searchSpace[2]
        topLeft = searchSpace[2]
#        topRight = searchSpace[2]
        
        cols = np.linspace(bottomLeft[1], bottomRight[1], num=ngrid)
        rows = np.linspace(bottomLeft[0], topLeft[0], num=ngrid)
        
        
        return cols, rows
    
    def rectangleZoneDefinition (self, searchSpace, latStepSize, lngStepSize):
        
        bottomLeft = searchSpace[0]
#        bottomRight = searchSpace[1]
        topLeft = searchSpace[3]
        topRight = searchSpace[2]
        
        rows = np.linspace(bottomLeft[0], topRight[0], num = latStepSize)
        cols = np.linspace(bottomLeft[1], topLeft[1], num = lngStepSize)
        
        return cols, rows
        
    
#    def rectangleZoneDefinition
        




def Distance(lon1, lat1, lon2, lat2):
    """    
    Distance is calculated between two points using radians traversed along the 
    radius of the earth. 
    
    Radius of Earth in km is 6371 km
    """
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    
    distance = 6371* c
    return distance



#distance = Distance(103.50,1.35,103.505,1.3505)


    




#%%

    
class NodeOptimizer():
    
    """
    Search Space class provides an search space object with zone definition method used to 
    grid the search space or the maps into many zones.
    
    Current method is to obtain a substantial space for the enablement of rental search space
    in the location.
    
    Each node then becomes a zone of interest.
    
    Node Optimizer is a class which initializes the zone of interest. Aim is to find the centroid
    of the square grid for ease of distance calculation as per the coordinates.
    
    """
    
    def __init__(self, nodeZone):
        """
        Each node is initialised with a unique x and y coordinates
        """
        self.verticeA = nodeZone[0]
        self.verticeB = nodeZone[1]
        self.verticeC = nodeZone[2]
        self.verticeD = nodeZone[3]
        
    def centroidZone(self):
        """
        Centroid Zone is the center lat & lng for the center of zone of interest.
        Center lat and lng to be used to estimate the Euclidean distance to each location of interest
        """
        centroidLat = self.verticeA[0] + (self.verticeB[0] - self.verticeA[0])/2
        centroidLng = self.verticeA[1] + (self.verticeC[1] - self.verticeA[1])/2
        
        return centroidLat, centroidLng
        
    def distanceCalculator(self, centroidLat, centroidLng, Latitude1, Longitude1):
        """
        Distance is calculated between two points using radians traversed along the 
        radius of the earth. 
    
        Radius of Earth in km is 6371 km
        """
        distanceList = []
        for Lat,Lng in zip(Latitude1, Longitude1):
            
            lon1, lat1, lon2, lat2 = map(radians, [centroidLng, centroidLat, Lng, Lat])
    
            dlon = lon2 - lon1 
            dlat = lat2 - lat1 
            
            a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
            c = 2 * asin(sqrt(a)) 
            
            distance = 6371* c
            
            distanceList.append(distance)
            
        return distanceList


    def ScoringMechanism(self, distanceList):
        """
        Score calculator for each node.
        """
        return sum([x for x in distanceList])  
    
    
    
#%%

"""
This relates to the backend algorithm using square search space model
"""
        
scoreList = []

if __name__ == '__main__':
    search_space = SearchSpace(Latitudes=Latitude1, Longitudes=Longitude1)
    square_search_space, stepSize = search_space.squareSearchSpace()
    lng, lat = search_space.squareZoneDefinition(square_search_space, stepSize)
    lat = lat.tolist()
    lng = lng.tolist()
    i = 0
    while i < len(lng):
        if i + 1 != stepSize:
            a = 0
            while a < len(lat):
                if a + 1 != stepSize:
                    nodeZone = [(lat[a], lng[i]),
                                (lat[a+1], lng[i]),
                                (lat[a+1], lng[i+1]),
                                (lat[a], lng[i+1])]
                    
                    node = NodeOptimizer(nodeZone)
                    centroidLat, centroidLng = node.centroidZone()
                    Distance_list = node.distanceCalculator(centroidLat, centroidLng, Latitude1, Longitude1)
                    nodeScore = node.ScoringMechanism(Distance_list)
                    scoreList.append([nodeScore, centroidLat, centroidLng])
                else:
                    pass
                a = a + 1
        else:
            pass
        i = i + 1
        
    
#%%

"""
This relates to the backend algorithm using rectangular search space model
"""
scoreList = []
if __name__ == '__main__':
    search_space = SearchSpace(Latitudes=Latitude1, Longitudes=Longitude1)
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
                    Distance_list = node.distanceCalculator(centroidLat, centroidLng, Latitude1, Longitude1)
                    nodeScore = node.ScoringMechanism(Distance_list)
                    scoreList.append([nodeScore, centroidLat, centroidLng])
                else:
                    pass
                a = a + 1
        else:
            pass
        i = i + 1
            
        
    
        
#%%
      




















#%%
scoreDf = pd.DataFrame()
scoreDf['NodeScore'] = [element[0] for element in scoreList]
scoreDf['Latitudes'] = [element[1] for element in scoreList]
scoreDf['Longitudes'] = [element[2] for element in scoreList]
scoreDf1 = scoreDf.drop_duplicates()
scoreDf1 = scoreDf1[scoreDf1.NodeScore == scoreDf1.NodeScore.min()]


#geocoder.osm("Tanjong Pagar Singapore")

    
    
    
    
    
    
    
#    for nodeLng in np.nditer(lng):
#        for nodeLat in np.nditer(lat):
#            nodeZone = [(nodeLat - 0.01, nodeLng - 0.01),
#                        (nodeLat, nodeLng - 0.01),
#                        (nodeLat, nodeLng),
#                        (nodeLat - 0.01, nodeLng)]
#            node = NodeOptimizer(nodeZone)
#            centroidLat, centroidLng = node.centroidZone()
#    
#    
#    
#    
#    
#    
#    
#    for nodeLat in np.nditer(lat):
#        i = 0
#        while i < stepSize:
#            if i == 0:
#                nodeZone = [(square_search_space[0][0],square_search_space[0][1]),
#                            ]
#    
#    
#    
#    
#    i = 0
#    while i < stepSize:
#        for nodeLat in np.nditer(lat):
#            nodeZone = [(nodeLat-0.01,)]
#            
            


        
    
#x = (2,3,4)
#y = (4,5,6)
#




#%%

import requests

url = "https://mashvisor-api.p.rapidapi.com/property"

querystring = {"id":"2430136","state":"CA"}

headers = {
    'x-rapidapi-host': "mashvisor-api.p.rapidapi.com",
    'x-rapidapi-key': "5aa76f9bf4mshfca9e6c56591f6ap1b78a1jsn2f916721f992"
    }

#response = requests.request("GET", url, headers=headers, params=querystring)

#print(response.text)
#%%


import json
import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

query_string='https://data.gov.sg/api/action/datastore_search?resource_id=5d03f34b-85cd-4929-8dd4-b60a488ac771&limit=5'
#resp = requests.get(query_string)
#Convert JSON into Python Object 
#data = json.loads(resp.content)

#%%

import requests

url = "https://hotels4.p.rapidapi.com/locations/search"

querystring = {"locale":"en_US","query":"new york"}

headers = {
    'x-rapidapi-host': "hotels4.p.rapidapi.com",
    'x-rapidapi-key': "5aa76f9bf4mshfca9e6c56591f6ap1b78a1jsn2f916721f992"
    }

#response = requests.request("GET", url, headers=headers, params=querystring)

#print(response.text)
