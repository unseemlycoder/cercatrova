import serial
ser = serial.Serial('/dev/ttyACM0', 9600)
sms=0
lat_done=0
lat=0
long=0
while 1: 
    if(ser.in_waiting >0):
        line = ser.readline()
        if b'+CMT:' in line:
            sms=1
            continue
        if sms==1:
            print(line.decode().strip())
            lat=line.decode().strip()
            lat_done=1
            sms=0