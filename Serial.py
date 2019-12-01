import serial
apikey = 'AIzaSyAvTQCGl03_PMRmJM6lFVWK7OI_GrdoYn8'
API_KEY = 'AIzaSyAvTQCGl03_PMRmJM6lFVWK7OI_GrdoYn8'
from googleplaces import GooglePlaces, types, lang 
import requests 
import json 
from math import sin, cos, sqrt, atan2, radians
google_places = GooglePlaces(API_KEY) 

def find(m,n):
    API_KEY = 'AIzaSyAvTQCGl03_PMRmJM6lFVWK7OI_GrdoYn8'
    lat_src=m
    long_src=n #college
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
    closest_hospital=a[0]
    #list

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
    return str(closest_hospital_lat)+','+str(closest_hospital_long)

ser = serial.Serial('/dev/ttyACM0', 9600)
sms=0
lat_done=0
lat=0
long=0
trig=1
while trig==1: 
    if(ser.in_waiting >0):
        line = ser.readline()
        if b'+CMT:' in line:
            sms=1
            print("c1")
            continue
        if sms==1 and lat_done!=1:
            print(line.decode().strip())
            lat=float(line.decode().strip())
            lat_done=1
            sms=0
            print("c2Lat")
            continue
        if lat_done==1 and sms==1:
            print(line.decode().strip())
            long=float(line.decode().strip())
            lat_done=0
            sms=0
            trig=0
            print("c3Long")
print(lat,long)
dest_cord=find(lat,long)

origin_dir=str(lat)+","+str(long)
destination_dir = dest_cord
#waypoints_dir = ['13.104043,77.583720','13.104043,77.583720']


from datetime import datetime
now = datetime.now()
import googlemaps
#### Setting u the API key to connect to Google maps API
apikey = 'AIzaSyAvTQCGl03_PMRmJM6lFVWK7OI_GrdoYn8'
#Perform request to use the Google Maps API web service
gmaps = googlemaps.Client(key=apikey)

#for i in waypoints_dir:
directions = gmaps.directions(origin = origin_dir,destination = destination_dir,mode='driving',departure_time = now)
dir=directions[0]['legs'][0]['steps']
import re,time
def cleanhtml(raw_html):
    cleanr=re.compile('<.*?>')
    cleantext=re.sub(cleanr,'',raw_html)
    return cleantext
s=["go-straight"]
for i in dir:
   for j,k in i.items():
        if 'maneuver' == j:
            print(k,sep= " ",end="")
            s.append(k)
        if 'html_instructions' == j: print(cleanhtml(k),sep= " ",end="")
        if 'start_location' ==j: print(k,sep= " ",end="")
        print()
print(s)
print("S1 S1 S3 S3")

if s[0]=="go-straight":
    print("First Maneuver:",s[0])
    ser.write(b'o12')
    time.sleep(15)
    ser.write(b'break\r\n')
    print('checkpoint')

if s[1]=="uturn-right":
    print("Second Maneuver:",s[1])
    ser.write(b'o11')
    time.sleep(15)
    ser.write(b'break\r\n')
    print('checkpoint')

if s[2]=="turn-right":
    print("Third Maneuver:",s[2])
    ser.write(b'o32')
    time.sleep(15)
    ser.write(b'break\r\n')
    print('checkpoint')
if s[3]=="turn-left":
    print("Fourth Maneuver:",s[3])
    ser.write(b'o31')
    time.sleep(15)
    ser.write(b'break\r\n')
    print('checkpoint')