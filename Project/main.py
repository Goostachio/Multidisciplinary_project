import csv
import sys
import time
from Adafruit_IO import MQTTClient
import requests
from sensors import sensor
from sensors import gps
#from camera import human_detector
from math import radians, sin, cos, sqrt, atan2

#Notice: the display for data analytics will use a local dashboard: Dash
import dash
from dash import html, dcc, Input, Output
import pandas as pd
from datetime import datetime, timezone
import dateutil.parser
#import requests
import plotly.express as px
#import csv
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template

AIO_FEED_ID = ["sensor1", "sensor2", "sensor3", "button1", "button2", "location"]
AIO_USERNAME = "Multidisciplinary_Project"
aio = open("/Users/daohongminh/Desktop/Project/Project/key/aio.txt")
serial = open("/Users/daohongminh/Desktop/Project/Project/key/aio_serial.txt")
AIO_KEY = aio.read()+serial.read()
aio.close()
serial.close()
AIO_IDs = ["sensor1", "sensor2", "sensor3", "button1", "button2", "location"]


location_to_check = (11.106550, 106.613027)  # VGU


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
temp_humid_coord_file = open("/Users/daohongminh/Desktop/Project/Project/data/temperature_humidity_coordinate.txt", "r")  # Open "temperature_humidity_coordinate.txt"
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

#initiate dash and its theme
app = dash.Dash(__name__,external_stylesheets=[dbc.themes.CYBORG])
load_figure_template('Cyborg')

"""the below codes refers to Dash's dashboards"""
#used for later
tick = 0 #live track time in sec
power_used = 0 #in kWh
morning = 0  # from 00:00 to 10:59
afternoon = 0  # from 11:00 to 17:59
evening = 0  # from 18:00 to 23:59

def changeFormat(date):
    return dateutil.parser.isoparse(date).astimezone()

def acPaymentCalc(watt): #from 4/5/2023
    if watt >=401:
        return watt*3015
    elif watt>=301:
        return watt*2919
    elif watt>=201:
        return watt*2612
    elif watt>=101:
        return watt*2074
    elif watt>=51:
        return watt*1786
    else:
        return watt*1728

def actualW(humidity):  #hudmidity may change ac's power input
    if (humidity>=40) & (humidity<=60):
        return 40
    elif (humidity>=20) | (humidity<=80):
        return 40*1.25
    else:
        return 40*1.75

def timeDeltaToday(date): #time since recorded time
    return datetime.combine(datetime.today(),datetime.today().time())- datetime.combine(changeFormat(date).date(),changeFormat(date).time())

# Layout
app.layout = html.Div([
    html.H1("Your AC statistics", style={'text-align': 'center'}),
    dcc.Interval(id='interval', interval = 2000),
    html.Div([
            # First column
            html.Div([
                dbc.Row(dbc.Col(
                    html.Div([
                        html.H3(children="Power used in this session (kWh):", className='box', style={'font-size': "24px", 'width': '100%', 'display': 'inline-block'}),
                        html.Div(id='power-used', children="0", className='box', style={'font-size': "12px", 'width': '100%', 'display': 'inline-block'}),
                    ])
                )
        ),
                dbc.Row(dbc.Col(
                    html.Div([
                        html.H3(children="Current payment this session (VND):", className='box', style={'font-size': "24px", 'width': '100%', 'display': 'inline-block'}),
                        html.Div(id='current-pay', children="0", className='box', style={'font-size': "12px",'width': '100%', 'display': 'inline-block'}),
                    ])
                )
        ),
            ], className="col-4"),

            # Second column
            html.Div([
                html.Div(children="Usage in the day", className='box', style={'font-size': "24px",'width': '100%', 'display': 'inline-block', 'color': 'white'}),
                html.Hr(style={"width": "50%", "margin": "auto"}),
                dcc.Graph(id='pie-chart', figure={}),
            ], className="col-8")
        ], className="row")])



# Callback for power used in session
@app.callback(
    Output('power-used', 'children'),
    Input('interval', 'n_intervals')
)

def update_power_used(n_intervals):
    #fetch api from button
    # define API endpoint and key
    url = "	https://io.adafruit.com/api/v2/Multidisciplinary_Project/feeds/button1"
    headers = {"X-AIO-Key": "aio_zdIq64LiUqWjsdEG0yWBsIJY73hS"}
    timeFrame = requests.get(url, headers=headers).json()

    #fetch api of humidity
    url = "https://io.adafruit.com/api/v2/Multidisciplinary_Project/feeds/sensor2"
    headers = {"X-AIO-Key": "aio_zdIq64LiUqWjsdEG0yWBsIJY73hS"}
    response = requests.get(url, headers=headers).json()
    humidity = int(float(response['last_value']))

    global power_used
    if int(timeFrame['last_value']) == 1:
        #track in second, this way will not reset the tick
        global tick
        tick +=1
    else:
        #when end, save payment in a .csv file
        payment = [changeFormat(timeFrame["created_at"]),power_used,acPaymentCalc(power_used)]

        #should be in a seperate func to save in a .csv file but don't work. pls help
        with open("pay.csv", 'a') as csvfile:
            # creating a csv writer object
            csvwriter = csv.writer(csvfile)

            # writing the data rows
            csvwriter.writerow(payment)

            # close file
            csvfile.close()

        tick=0


    power_used += (tick/3600)*(actualW(humidity)/1000)
    return html.H2(f"{power_used:.2f} (kWh)") #in kWs


# Callback for current pay this month
@app.callback(
    Output('current-pay', 'children'),
    Input('power-used', 'children')
)


def update_current_pay(power_used):
    # fetch api of humidity
    url = "https://io.adafruit.com/api/v2/Multidisciplinary_Project/feeds/sensor2"
    headers = {"X-AIO-Key": "aio_zdIq64LiUqWjsdEG0yWBsIJY73hS"}
    response = requests.get(url, headers=headers).json()
    humidity = int(float(response['last_value']))

    global current_pay
    current_pay = 0
    if power_used:
        power_used = (tick/3600)*(actualW(humidity)/1000)
        current_pay += acPaymentCalc(power_used)

        return html.H2(f"{current_pay:.2f} (VND) ")

    return html.H2("0 (VND)")


# Callback for pie chart
@app.callback(
    Output('pie-chart', 'figure'),
    Input('interval', 'n_intervals')
)

def update_pie_chart(n_intervals):
    # fetch api from button
    # define API endpoint and key
    url = "	https://io.adafruit.com/api/v2/Multidisciplinary_Project/feeds/button1"
    headers = {"X-AIO-Key": "aio_zdIq64LiUqWjsdEG0yWBsIJY73hS"}
    timeFrame = requests.get(url, headers=headers).json()

    global morning
    global afternoon
    global evening

    if timeFrame['last_value'] == "1":
        #current_time = timeFrame['created_at'] + timeDeltaToday(changeFormat(timeFrame['created_at']))
        if timeDeltaToday(timeFrame['created_at']).days >0:
            #reset morning, afternoon and evening values and save to a csv file at midnight
            # should be in a seperate func to save in a .csv file but don't work. pls help
            tracking = [changeFormat(timeFrame["created_at"]).date(),morning,afternoon,evening]
            with open("usage_tracking.csv", 'a') as csvfile:
                # creating a csv writer object
                csvwriter = csv.writer(csvfile)

                # writing the data rows
                csvwriter.writerow(tracking)

                # close file
                csvfile.close()

            morning, afternoon, evening= 0, 0, 0
        elif (changeFormat(timeFrame['created_at']).hour >=0) & (changeFormat(timeFrame['created_at']).hour <=10):
            morning += 1
        elif (changeFormat(timeFrame['created_at']).hour >=11) & (changeFormat(timeFrame['created_at']).hour <=17):
            afternoon += 1
        else:
            evening +=1
        df = pd.DataFrame(data=[["morning",morning],["afternoon",afternoon],["evening",evening]],columns=["Time of the day",'Duration'])
        fig = px.pie(df,values="Duration",names="Time of the day", title="Usage of today")
        return fig

#starting Dash
if __name__ == '__main__':
    app.run_server(debug=True)

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

        print(f'Latitude: {latitude}, Longitude: {longitude}')
        time.sleep(1)

    #human_detector_result = human_detector.detection()

    client.publish("sensor1", temperature)
    client.publish("sensor2", humidity)
    #client.publish("ai", human_detector_result)
    publish_gps_to_adafruit_io(latitude, longitude)
    distance = calculate_distance(location_to_check[0], location_to_check[1], latitude, longitude)
    print("Distance: ", distance)
    #human_detector_result = human_detector.detection()

    time.sleep(2)

    # ON/OFF AUTOMATION LOGIC human_detector_result == "Human presence" and
    if  temperature > 28:  # First if block -> tag = 0
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

    elif distance > 1  :
        # print("If Block 3 true") and human_detector_result == "Empty"
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


