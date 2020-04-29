"""
Created on Mon Mar 23 06:45:46 2020

@author: ankei
"""


"""
Method using nominatium

"""
addr = "460 corporation road singapore"
def geocode_fetch_lat_long(addr):
    from geopy.geocoders import Nominatim
    geolocator = Nominatim(user_agent="RoadWarriors")
    location = geolocator.geocode(address)
   """
    print(location.address)
    print((location.latitude, location.longitude)) 
    print(location.raw)
   """ 
    addr.address = location.address
    addr.lat = location.latitude
    addr.long = location.longitude
    addr.raw = location.raw
    
    return(addr.address)
    return(addr.lat)
    return(addr.long)
    return(addr.raw)

print(addr.address)

"""
Reverse lookup definition


"""

from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="RoadWarriors")
location = geolocator.reverse("52.509669, 13.376294")
print(location.address)
print((location.latitude, location.longitude))
print(location.raw)



from geopy.distance import geodesic
newport_ri = (41.49008, -71.312796)
cleveland_oh = (41.499498, -81.695391)
print(geodesic(newport_ri, cleveland_oh).miles)
