import random
import serial


# Define the serial port and baud rate to match the Arduino
SERIAL_PORT = '/dev/ttyUSB0'  # Replace with the actual serial port for your Arduino
BAUD_RATE = 9600

# Define the bounding box for generating random GPS coordinates
BEN_CAT_GPS_REGION = {
    'min_lat': 11.072128,  # Minimum latitude (approximate latitude of Thị Tính river)
    'max_lat': 11.134877,  # Maximum latitude (approximate latitude of Vitadairy Binh Duong factory)
    'min_lon': 106.580999,  # Minimum longitude (approximate longitude of Café Tiến Anh)
    'max_lon': 106.658452   # Maximum longitude (approximate longitude of Miếu Bà)
}

def read_gps_data():
    try:
        with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1) as ser:
            while True:
                line = ser.readline().decode('utf-8').strip()
                if line.startswith("Latitude= ") and line.count(" Longitude= ") == 1:
                    # Extract latitude and longitude values from the line
                    _, lat_str, lon_str = line.split()
                    latitude = float(lat_str)
                    longitude = float(lon_str)
                    return latitude, longitude
    except serial.SerialException:
        # Serial port not accessible, generate random GPS coordinates instead
        latitude = round(random.uniform(BEN_CAT_GPS_REGION['min_lat'], BEN_CAT_GPS_REGION['max_lat']), 6)
        longitude = round(random.uniform(BEN_CAT_GPS_REGION['min_lon'], BEN_CAT_GPS_REGION['max_lon']), 6)
        return latitude, longitude

#mqtt
#try:
#    while True:
#        latitude, longitude = read_gps_data()
#        print(f"Latitude: {latitude}, Longitude: {longitude}")
#
#        # Save both GPS coordinates to the text file
#        with open('gps_coordinates.txt', 'a') as file:
#            file.write(f"{latitude},{longitude}\n")

#        time.sleep(1)
#
#except KeyboardInterrupt:
#    print("Keyboard interrupt. Stopping...")
