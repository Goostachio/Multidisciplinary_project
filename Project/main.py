import csv
import sys
import time
from Adafruit_IO import MQTTClient
import requests
from sensors import sensor
from sensors import gps
from camera import human_detector
from math import radians, sin, cos, sqrt, atan2



AIO_FEED_ID = ["sensor1", "sensor2", "sensor3", "button1", "button2", "location"]
AIO_USERNAME = "Multidisciplinary_Project"
aio = open("key/aio.txt")
serial = open("key/aio_serial.txt")
AIO_KEY = aio.read()+serial.read()
aio.close()
serial.close()
AIO_IDs = ["sensor1", "sensor2", "sensor3", "button1", "button2", "location"]


def connected(this_client):
    print("Ket noi thanh cong ...")
    for i in AIO_IDs:
        this_client.subscribe(i)


def subscribe(this_client, userdata, mid, granted_qos):
    print("Subscribe thanh cong ...")


def disconnected(this_client):
    print("Ngat ket noi ...")
    sys.exit(1)


def message(this_client, feed_id, payload):
    print("Nhan du lieu: " + feed_id + " " + payload)



def init_global_equation():
    headers = {}
    aio_url = "https://io.adafruit.com/api/v2/Multidisciplinary_Project/feeds/equation"
    x = requests.get(url=aio_url, headers=headers, verify=False)
    data = x.json()
    global global_equation
    global_equation = data["last_value"]
    print("Get latest value:", global_equation)




def publish_gps_to_adafruit_io(latitude, longitude):

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


def calculate_distance(lat1, lon1, lat2, lon2):
    r = 6371.0  # Earth's radius in kilometers

    lat1_rad = radians(lat1)
    lon1_rad = radians(lon1)
    lat2_rad = radians(lat2)
    lon2_rad = radians(lon2)

    d_lon = lon2_rad - lon1_rad
    d_lat = lat2_rad - lat1_rad

    a = sin(d_lat / 2)**2 + cos(lat1_rad) * cos(lat2_rad) * sin(d_lon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    this_distance = r * c
    return this_distance

location_to_check = (11.106550, 106.613027)  # VGU


def request_data(cmd):
    sensor.send_command(cmd)
    time.sleep(2)
    temp_hum = sensor.read_serial()

    return temp_hum


client = MQTTClient(AIO_USERNAME, AIO_KEY)

client.on_connect = connected
client.on_disconnect = disconnected
client.on_message = message
client.on_subscribe = subscribe
client.connect()
client.loop_background()


on_off_second = 0  # When a certain value is reached, depends on the situation, the AC functions accordingly
on_off_tag = 0  # Mark at which 'ON/OFF AUTOMATION' condition block the code was run from

mode_second = 0  # When a certain value is reached, depends on the situation, the AC functions accordingly
mode_tag = 0  # Mark at which 'MODE AUTOMATION' condition block the code was run from

trigger_point = 100  # RELATE TO __second variable above (help with maintenance purposes)
is_on = False  # To tell whether the AC is on or off


counter = 0  # Use to get the index of the below 2 lists
temp_humid_coord_file = open("data/temperature_humidity_coordinate.txt", "r")  # Open "temperature_humidity_coordinate.txt"
temp_humid_coord_list = list(csv.reader(temp_humid_coord_file))  # Create a list (array) from temp_humid_file CSV (easier for me to work with)
temp_humid_coord_length = len(temp_humid_coord_list)  # Size of array
temp_humid_coord_file.close()


def is_previous_on_off_if_block(this_tag):  # Read explanation in the ON/OFF AUTOMATION LOGIC for better understanding
    global on_off_tag
    global on_off_second
    if this_tag != on_off_tag:
        on_off_tag = this_tag
        on_off_second = 0
    on_off_second += 10


def is_previous_mode_if_block(this_tag):  # Read explanation in the ON/OFF AUTOMATION LOGIC for better understanding
    global mode_tag
    global mode_second
    if this_tag != mode_tag:
        mode_tag = this_tag
        mode_second = 0
    mode_second += 10



#main app
while True:
    if sensor.USE_REAL_SENSOR_DATA:

        temperature = request_data("0")
        humidity = request_data("1")
        latitude, longitude = gps.read_gps_data(float(temp_humid_coord_list[counter][2]),
                                                float(temp_humid_coord_list[counter][3]))
        time.sleep(1)
    else:


        # Read value from files
        temperature = float(temp_humid_coord_list[counter][0].strip())  # The 2nd dimension index has to be 0
        humidity = float(temp_humid_coord_list[counter][1].strip())  # The 2nd dimension index has to be 1
        latitude, longitude = gps.read_gps_data(float(temp_humid_coord_list[counter][2]),
                                                float(temp_humid_coord_list[counter][3]))
        counter += 1
        if counter > temp_humid_coord_length:  # Loop back from the beginning when reach the end
            counter = 0

        print("Can not open the port. Using simulated data.") # print message
        print(f'Latitude: {latitude}, Longitude: {longitude}')
        time.sleep(1)

    human_detector_result = human_detector.detection()

    client.publish("sensor1", temperature)
    client.publish("sensor2", humidity)
    client.publish("ai", human_detector_result)
    publish_gps_to_adafruit_io(latitude, longitude)
    distance = calculate_distance(location_to_check[0], location_to_check[1], latitude, longitude)
    print("Distance: ", distance)
    human_detector_result = human_detector.detection()

    time.sleep(2)

    # ON/OFF AUTOMATION LOGIC                          
    if human_detector_result == "Human presence" and temperature > 28:  # First if block -> tag = 0
        # If the tag is not equal to 0 (the first if block) set 'tag' to 0 and reset 'second' to 0
        # This prevents conflict between each if block. For example, if the 1st 'if block' is only
        # executed half way (second = 200)
        # And the 4th 'if block' is executed, the code should know to set 'second' back to 0 so that the 4th if block
        # can be executed correctly (if 'second' is not set to 0 the instruction will be run immediately, which defeats
        # the 60-second delay logic)
        # But when a 'if block' is executed consecutively, then 'second' should not be set back to 0
        # print("If Block 0 true")
        is_previous_on_off_if_block(0)  # First if block -> on_off_tag = 0

        if on_off_second > trigger_point/5:
            client.publish("button1", "1")
            on_off_second = 0
            is_on = True

    elif distance <= 1 and temperature > 28:
        # print("If Block 1 true")
        is_previous_on_off_if_block(1)  # Second if block -> on_off_tag = 1
        if on_off_second > trigger_point/5:
            client.publish("button1", "1")
            on_off_second = 0
            if_on = True

    elif temperature < 24:
        # print("If Block 2 true")
        is_previous_on_off_if_block(2)  # Third if block -> on_off_tag = 2
        if on_off_second > trigger_point/5:
            client.publish("button1", "0")
            on_off_second = 0
            is_on = False

    elif distance > 1 and human_detector_result == "Empty" :
        # print("If Block 3 true")        
        is_previous_on_off_if_block(3)  # Fourth if block -> on_off_tag = 3
        if on_off_second > trigger_point/5:
            client.publish("button1", "0")
            on_off_second = 0
            is_on = False

    # MODE AUTOMATION LOGIC
    if is_on is True and humidity > 70:
        is_previous_mode_if_block(0)  # First if block -> mode_tag = 0
        if mode_second > trigger_point/5:
            client.publish("button2", "1")
            mode_second = 0
    elif is_on is False and humidity <= 70:
        is_previous_mode_if_block(1)  # Second if block -> mode_tag = 1
        if mode_second > trigger_point/5:
            client.publish("button2", "0")
            mode_second = 0

    time.sleep(10)

    pass


