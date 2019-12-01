apikey = 'AIzaSyAvTQCGl03_PMRmJM6lFVWK7OI_GrdoYn8'
from googleplaces import GooglePlaces, types, lang 
import requests 
import json 
from math import sin, cos, sqrt, atan2, radians

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
lat_src=12.861806 
long_src=77.664670 #college
lat_long=str(lat_src)+","+str(long_src)
#print(lat_long)

# Initialising the GooglePlaces constructor 
google_places = GooglePlaces(API_KEY) 

# call the function nearby search with 
# the parameters as longitude, latitude, 
# radius and type of place which needs to be searched of 
# type can be HOSPITAL, CAFE, BAR, CASINO, etc 
query_result = google_places.nearby_search( 
		# lat_lng ={'lat': 46.1667, 'lng': -1.15}, 
		lat_lng ={'lat': lat_src, 'lng': long_src}, 
		radius = 5000, 
		# types =[types.TYPE_HOSPITAL] or 
		# [types.TYPE_CAFE] or [type.TYPE_BAR] 
		# or [type.TYPE_CASINO]) 
		types =[types.TYPE_HOSPITAL]) 

# If any attributions related 
# with search results print them 
if query_result.has_attributions: 
	print (query_result.html_attributions) 

loc_data=[]

# Iterate over the search results 
for place in query_result.places: 
	# print(type(place)) 
	# place.get_details() 
	#print (place.name) 
    lat_place=place.geo_location['lat']
    long_place=place.geo_location['lng']
    R = 6373.0

    lat1 = radians(lat_src)
    lon1 = radians(long_src)
    lat2 = radians(lat_place)
    lon2 = radians(long_place)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c
    loc_data.append([place.name,lat_place,long_place,distance])
    


  #  print("Latitude", place.geo_location['lat']) 
  #  print("Longitude", place.geo_location['lng']) 
   # print() 

a = sorted(loc_data, key=lambda x: x[3])
#print(a)
closest_hospital=a[0]#list

#destination coordinates
#closest_hospital_lat=a[0][1] 
# closest_hospital_long=a[0][2]

# print(closest_hospital_lat)
# print(closest_hospital_long)
for j in a:
    if('Hospital' in j[0]):
        print("The nearest hospital is: ")
        print(j[0])
        closest_hospital_lat=j[1]
        closest_hospital_long=j[2]
        break;
closest_hospital_coord=str(closest_hospital_lat)+','+str(closest_hospital_long)