import gmaps
import gmaps.datasets
gmaps.configure(api_key='AIzaSyAvTQCGl03_PMRmJM6lFVWK7OI_GrdoYn8')

# Latitude-longitude pairs
origin = (12.861806,77.664670)
destination = (12.870464,77.659501)

trashcans = [(12.863914,77.656840)]

fig = gmaps.figure()
route = gmaps.directions_layer(origin,destination,waypoints=trashcans)
fig.add_layer(route)
fig