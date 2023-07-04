print("sensor und actuator")
import time
import serial.tools.list_ports


try:
    ser = serial.Serial(port="/dev/tty.usbserial-110", baudrate=115200)
except:
    print("Can not open the port")

def sendCommand(cmd): 
    ser.write(cmd.encode())

mess = ""
def processData(data):
    data = data.replace("!", "") 
    data = data.replace("#", "")
    splitData = data.split(":") 
    print(splitData)


def readSerial():
    bytesToRead = ser.inWaiting() 
    if (bytesToRead > 0):
        global mess
        mess = mess + ser.read(bytesToRead).decode("UTF-8") 
        
        while ("#" in mess) and ("!" in mess):
            start = mess.find("!")
            end = mess.find("#") 
            return_Data = processData(mess[start:end + 1]) 
            if (end == len(mess)):
                mess = "" 
            else:
                mess = mess[end+1:]
    return return_Data

#def requestData(cmd): 
#    sendCommand(cmd) 
#    time.sleep(1) 
#    readSerial()


#while True:
#    print("Testing commands") 
#    sendCommand("2") 
#    time.sleep(2) 
#    sendCommand("3") 
#    time.sleep(2) 
#    sendCommand("4") 
#    time.sleep(2) 
#    sendCommand("5") 
#    time.sleep(2)