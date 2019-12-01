# cercatrova
Kalpana Hackathon Project

Problem Statement
One of the crucial issues for emergency medical service (EMS) in metropolis city is traffic congestion. Especially, the ambulance services are highly affected. Their response time increases leading to the causes of death and disabilities of patients in crisis, which impose severe socio-economic costs across the world. Devise a solution using technology to manage traffic for the ambulance to reach faster.

Our solution to this problem is to have a service that would map out the shortest path between the ambulance and destination. The ambulance sends out its co-ordinates through GPS. These co-ordinates are then matched with the geo-fence of the traffic lights. As the ambulance approaches the geo-fence, the lights turn green to allow the ambulance to pass. Upon leaving this fence, the traffic lights switch back to its original algorithm. 

Geo-fence matching is done using Google Maps API, the co- ordinates of the ambulance is sent using an Arduino with a GSM module capable of sending GPS Lat-Long data. The traffic lights are connected to a local server by means of a Raspberry Pi. A Centralized Server connects all the Traffic Light Nodes together. This should ensure quick response time of emergency services.
