import time
import serial.tools.list_ports
import random

try:
    ser = serial.Serial(port="/dev/tty.usbserial-1130", baudrate=115200)
except:
    print("Can not open the port. Using simulated data.")
    USE_REAL_SENSOR_DATA = False

def sendCommand(cmd): 
    ser.write(cmd.encode())

def generateRandomTH():
    # Generate random temperature (T) and humidity (H) values
    random_temperature = round(random.uniform(10, 40), 2)  # Random temperature between 10 and 40 degrees Celsius
    random_humidity = round(random.uniform(10, 80), 2)     # Random humidity between 10% and 80%
    return random_temperature, random_humidity

mess = ""
def processData(data):
    data = data.replace("!", "") 
    data = data.replace("#", "")
    splitData = data.split(":") 
    
    if len(splitData) == 3 and splitData[1] in ['H', 'T']:
        try:
            sensor_value = float(splitData[2])
            return sensor_value
        except ValueError:
            print("Error: Sensor data is not a numeric value.")
    return None 


def readSerial():
    bytesToRead = ser.inWaiting()
    global mess
    returnData = ""
    if bytesToRead > 0:
        mess = mess + ser.read(bytesToRead).decode("UTF-8")

        while "#" in mess and "!" in mess:
            start = mess.find("!")
            end = mess.find("#")
            returnData = processData(mess[start:end+1])

            if (end == len(mess)):
                mess = ""
            else: 
                mess = mess[end+1:]

    return returnData
       

#mttq
def requestData(cmd): 
    sendCommand(cmd) 
    time.sleep(1) 
    readSerial()













