import sys
import time
import random
from Adafruit_IO import MQTTClient



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

client = MQTTClient(AIO_USERNAME , AIO_KEY)


client.on_connect = connected
client.on_disconnect = disconnected
client.on_message = message
client.on_subscribe = subscribe
client.connect()
client.loop_background()


while True:
    #time.sleep(5)
    #client.publish("sensor1", random.randint(0, 101))
    #client.publish("sensor2", random.randint(0, 101))
    #client.publish("sensor3", random.randint(0, 21))    
    pass