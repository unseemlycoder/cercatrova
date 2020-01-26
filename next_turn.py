origin_dir='13.119076,77.579578'
destination_dir = '13.104043,77.583720'
waypoints_dir = ['13.104043,77.583720','13.104043,77.583720']


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

for i in dir:
   for j,k in i.items():
        if 'maneuver' == j: print(k,sep= " ",end="")
        if 'html_instructions' == j: print(k,sep= " ",end="")
        if 'start_location' ==j: print(k,sep= " ",end="")
        print()