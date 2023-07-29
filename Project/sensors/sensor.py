# Import required library
import serial.tools.list_ports

# Function to find the connected port name
def get_port():
    # Get a list of available serial ports
    ports = serial.tools.list_ports.comports()
    n = len(ports)
    comm_port = "None"
    for i in range(0, n):
        port = ports[i]
        str_port = str(port)

         # Check if the description of the port contains "USB Serial Device"
        if "USB Serial Device" in str_port:
            split_port = str_port.split(" ")
            comm_port = (split_port[0])
    return comm_port


try: # Try to open a serial connection with the obtained port and set the baud rate to 115200
    ser = serial.Serial(port=get_port(), baudrate=115200)

except: # If the connection cannot be established
    print("Can not open the port. Using simulated data.") # print message
    USE_REAL_SENSOR_DATA = False 
    # set to be False to indicate that ports couldn't be accessed (main source code will use this as a condition)

# Function to send a command to the connected device through the serial port
def send_command(cmd):
    ser.write(cmd.encode())

# Variable to store incoming data from the serial port
mess = ""

# Function to process data received from the serial port
def process_data(data):
    # Remove special characters from the data
    data = data.replace("!", "")
    data = data.replace("#", "")
    # Split the data into parts based on colon (:)
    split_data = data.split(":")

    # Check if the data is in the expected format and contains humidity (H) or temperature (T) values
    if len(split_data) == 3 and split_data[1] in ['H', 'T']:
        try:
            # Convert the sensor value to a floating-point number
            sensor_value = float(split_data[2])
            return sensor_value
        except ValueError:
            # Print an error message if the sensor data is not numeric
            print("Error: Sensor data is not a numeric value.")
    return None

# Function to read data from the serial port and process it
def read_serial():
    # Check the number of bytes available to read from the serial port
    bytes_to_read = ser.inWaiting()
    global mess
    return_data = ""
    if bytes_to_read > 0:
        # Read the data from the serial port and decode it to a string
        mess = mess + ser.read(bytes_to_read).decode("UTF-8")

        # Check if the data contains start and end markers ('!' and '#')
        while "#" in mess and "!" in mess:
            # Find the positions of the start and end markers
            start = mess.find("!")
            end = mess.find("#")
            # Extract the data between the markers and process it
            return_data = process_data(mess[start:end + 1])

            # Update the remaining data in 'mess' variable
            if end == len(mess):
                mess = ""
            else:
                mess = mess[end+1:]

    return return_data


