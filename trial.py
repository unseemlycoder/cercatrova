from googleplaces import GooglePlaces, types, lang 
import requests 
import json 

# This is the way to make api requests 
# using python requests library 

# send_url = 'http://freegeoip.net/json' 
# r = requests.get(send_url) 
# j = json.loads(r.text) 
# print(j) 
# lat = j['latitude'] 
# lon = j['longitude'] 

# Generate an API key by going to this location 
# https://cloud.google.com /maps-platform/places/?apis = 
# places in the google developers 

# Use your own API key for making api request calls 
API_KEY = 'AIzaSyAvTQCGl03_PMRmJM6lFVWK7OI_GrdoYn8'
apikey = 'AIzaSyAvTQCGl03_PMRmJM6lFVWK7OI_GrdoYn8'

# Initialising the GooglePlaces constructor 
google_places = GooglePlaces(API_KEY) 

# call the function nearby search with 
# the parameters as longitude, latitude, 
# radius and type of place which needs to be searched of 
# type can be HOSPITAL, CAFE, BAR, CASINO, etc 
query_result = google_places.nearby_search( 
        # lat_lng ={'lat': 46.1667, 'lng': -1.15}, 
        lat_lng ={'lat': 28.4089, 'lng': 77.3178}, 
        radius = 5000, 
        # types =[types.TYPE_HOSPITAL] or 
        # [types.TYPE_CAFE] or [type.TYPE_BAR] 
        # or [type.TYPE_CASINO]) 
        types =[types.TYPE_HOSPITAL]) 

# If any attributions related 
# with search results print them 
if query_result.has_attributions: 
    print (query_result.html_attributions) 


# Iterate over the search results 
for place in query_result.places: 
    # print(type(place)) 
    # place.get_details() 
    print (place.name) 
    print("Latitude", place.geo_location['lat']) 
    print("Longitude", place.geo_location['lng']) 
    print()
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

point = Point(0.65, 0.65)
polygon = Polygon([(0, 0), (0, 1), (1, 1),(0,1)])
print(polygon.contains(point))

origin=(13.119076,77.579578)
destination = (13.104043,77.583720)
waypoints = [(13.104043,77.583720)] 

import gmaps
from datetime import datetime
now = datetime.now()

#configure api
gmaps.configure(api_key=apikey)

#Create the map
fig = gmaps.figure()
#create the layer on the map 
layer = gmaps.directions.Directions(origin, destination,
                                    mode='car',api_key=apikey,departure_time = now)
#Add the layer
fig.add_layer(layer)
print(fig)

