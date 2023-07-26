import time
import serial.tools.list_ports
import random


# find connected port name
def get_port():
    ports = serial.tools.list_ports.comports()
    n = len(ports)
    comm_port = "None"
    for i in range(0, n):
        port = ports[i]
        str_port = str(port)
        if "USB Serial Device" in str_port:
            split_port = str_port.split(" ")
            comm_port = (split_port[0])
    return comm_port


try:
    ser = serial.Serial(port=get_port(), baudrate=115200)
except:
    print("Can not open the port. Using simulated data.")
    USE_REAL_SENSOR_DATA = False


def send_command(cmd):
    ser.write(cmd.encode())


def generate_random_temp_humid():
    # Generate random temperature (T) and humidity (H) values
    random_temperature = round(random.uniform(10, 40), 2)  # Random temperature between 10 and 40 degrees Celsius
    random_humidity = round(random.uniform(10, 80), 2)     # Random humidity between 10% and 80%
    return random_temperature, random_humidity


mess = ""


def process_data(data):
    data = data.replace("!", "")
    data = data.replace("#", "")
    split_data = data.split(":")

    if len(split_data) == 3 and split_data[1] in ['H', 'T']:
        try:
            sensor_value = float(split_data[2])
            return sensor_value
        except ValueError:
            print("Error: Sensor data is not a numeric value.")
    return None


def read_serial():
    bytes_to_read = ser.inWaiting()
    global mess
    return_data = ""
    if bytes_to_read > 0:
        mess = mess + ser.read(bytes_to_read).decode("UTF-8")

        while "#" in mess and "!" in mess:
            start = mess.find("!")
            end = mess.find("#")
            return_data = process_data(mess[start:end + 1])

            if end == len(mess):
                mess = ""
            else:
                mess = mess[end+1:]

    return return_data


# MTTQ
def request_data(cmd):
    send_command(cmd)
    time.sleep(1)
    read_serial()
