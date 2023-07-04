import sys
import time
import random
from Adafruit_IO import MQTTClient
import requests
import sensor


AIO_FEED_ID = ["sensor1", "sensor2", "sensor3", "button1", "button2","equation"]
AIO_USERNAME = "Multidisciplinary_Project"
AIO_KEY = ""
AIO_IDs=["sensor1", "sensor2", "sensor3", "button1", "button2", "equation"]

global_equation=""

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

def request_Data(command):
    sensor.sendCommand(command)
    time.sleep(3)
    return_Data = sensor.readSerial()
    if return_Data ==[]:
        return "0"
    return return_Data[2]

client = MQTTClient(AIO_USERNAME , AIO_KEY)


client.on_connect = connected
client.on_disconnect = disconnected
client.on_message = message
client.on_subscribe = subscribe
client.connect()
client.loop_background()
init_glogal_equation()


while True:
    time.sleep(5)
    s1=float(request_Data("0"))
    s2=float(request_Data("1"))
    s3=random.randint(0, 101)
    client.publish("sensor1", s1)
    client.publish("sensor2", s2)
    client.publish("sensor3", s3)
    client.publish("test feed", modify_value (s1,s2,s3))

    pass