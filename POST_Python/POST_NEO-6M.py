import serial
from time import sleep
from datetime import datetime

# Raspberry Pi hardware serial port
serial_port = "/dev/ttyS0"

# Baudrate
baud_rate = 9600

# Create a serial object
ser = serial.Serial(serial_port, baud_rate)

def parseGPS(data):
    # Split the data into individual parts
    parts = data.decode().split(",")
    if parts[0] == "$GPRMC":
        if parts[2] == 'V':
            print("No satellite data available")
            return
        time = parts[1][0:6]
        lat = decode(parts[3])
        lon = decode(parts[5])
        print("Time: %s, Latitude: %s, Longitude: %s" % (time, lat, lon))

def decode(coord):
    # Convert coordinates to degrees
    # Example: coord: 4124.8963 -> 41.4132718
    return float(coord[0:2]) + (float(coord[2:]) / 60.0)

try:
    while True:
        data = ser.readline()
        parseGPS(data)

except KeyboardInterrupt:
    print("Program terminated by user")

finally:
    ser.close()
