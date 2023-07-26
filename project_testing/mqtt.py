import sys
import time
import random
from Adafruit_IO import MQTTClient
import requests
import sensor
import gps
from math import radians, sin, cos, sqrt, atan2


AIO_FEED_ID = ["sensor1", "sensor2", "sensor3", "button1", "button2","equation","location"]
AIO_USERNAME = "Multidisciplinary_Project"
AIO_KEY = "aio_jeoa49rlUiJYm1nSxDarn7PamnGO"
AIO_IDs=["sensor1", "sensor2", "sensor3", "button1", "button2", "equation","location"]

global_equation="x1+x2+x3"
location_to_check = (11.106550, 106.613027)  #VGU


def connected(client):
    print("Ket noi thanh cong ...")
    for i in AIO_IDs:
        client.subscribe(i)

def subscribe(client , userdata , mid , granted_qos):
    print("Subscribe thanh cong ...")

def disconnected(client):
    print("Ngat ket noi ...")
    sys.exit (1)

def message(client , feed_id , payload):
    print("Nhan du lieu: " + payload)

    if(feed_id == "equation"):
        global_equation = payload
        print(global_equation)
        return
    
    if (feed_id == "button1"):
        if payload == "ON":
            print("Bat den...")
            sensor.sendCommand("2")
            return
        
        if payload == "OFF":
            print("Tat den...")
            sensor.sendCommand("3")
            return
    


def init_glogal_equation():
    headers={}
    aio_url="https://io.adafruit.com/api/v2/Multidisciplinary_Project/feeds/equation"
    x = requests.get(url=aio_url, headers=headers, verify=False)
    data=x.json()
    global_equation = data["last_value"]
    print("Get lastest value:", global_equation)

def modify_value(x1,x2,x3):
    result = eval(global_equation)
    print(result)
    return result


def publish_gps_to_adafruit_io(latitude, longitude):
    #latitude_str = str(latitude)
    #longitude_str = str(longitude)

    aio_headers = {
        'X-AIO-Key': AIO_KEY,
        'Content-Type': 'application/json',
    }
    aio_url = f'https://io.adafruit.com/api/v2/Multidisciplinary_Project/feeds/location/data'
    aio_payload = {
        'value': f'{latitude},{longitude}',
    }
    response = requests.post(aio_url, headers=aio_headers, json=aio_payload)
    if response.status_code == 200:
        print(f'Published GPS data: Latitude={latitude}, Longitude={longitude}')
    else:
        print(f'Failed to publish GPS data. Status code: {response.status_code}')


# Time frame (in seconds)
time_frame = 60

# Minimum distance threshold (in meters)
min_distance_threshold = 10

def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371.0  # Earth's radius in kilometers

    lat1_rad = radians(lat1)
    lon1_rad = radians(lon1)
    lat2_rad = radians(lat2)
    lon2_rad = radians(lon2)

    d_lon = lon2_rad - lon1_rad
    d_lat = lat2_rad - lat1_rad

    a = sin(d_lat / 2)**2 + cos(lat1_rad) * cos(lat2_rad) * sin(d_lon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c * 1000
    return distance
    


def requestData(cmd): 
    sensor.sendCommand(cmd) 
    time.sleep(2)
    temp_hum = sensor.readSerial()
    
    return temp_hum
    
    

client = MQTTClient(AIO_USERNAME , AIO_KEY)


client.on_connect = connected
client.on_disconnect = disconnected
client.on_message = message
client.on_subscribe = subscribe
client.connect()
client.loop_background()
init_glogal_equation()


while True:

    if sensor.USE_REAL_SENSOR_DATA:

        s1 = requestData ("0")
        s2 = requestData("1")
        time.sleep(1)
    else:

        s1, s2 = sensor.generateRandomTH()
        time.sleep(1)

    s3=random.randint(0, 101)
    client.publish("sensor1", s1)
    client.publish("sensor2", s2)
    client.publish("sensor3", s3)
    time.sleep(2)
    client.publish("test feed", modify_value (s1,s2,s3))

    latitude, longitude = gps.read_gps_data()
    print(f'Latitude: {latitude}, Longitude: {longitude}')
    publish_gps_to_adafruit_io(latitude, longitude)
    
    start_time = time.time()

    # Calculate the distance to the target coordinates
    distance_to_target = calculate_distance(latitude, longitude,location_to_check[0], location_to_check[1])

    # Check if GPS is getting closer or further away from the target
    if distance_to_target < min_distance_threshold:
        print("GPS is getting closer (1)")
    else:
        print("GPS is getting further away (0)")

    # Check the time elapsed in the time frame
 

#    distance = calculate_distance(location_to_check[0], location_to_check[1], latitude, longitude)
#    if distance <= 3:
#        client.publish("button1","1")
#    else:
#        client.publish("button1","0")


    time.sleep(10)

    pass