import serial

# Serial port settings for GPS module
SERIAL_PORT = ''  # Replace with the actual serial port for your GPS module
BAUD_RATE = 9600

# Function to read GPS data from the serial port and save it to a text file
def read_and_save_gps_data(filename):
    with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1) as ser:
        while True:
            line = ser.readline().decode('utf-8').strip()
            if line.startswith('$GPGGA'):
                gps_data = line.split(',')
                latitude = float(gps_data[2])
                longitude = float(gps_data[4])
                with open(filename, 'a') as file:
                    file.write(f"{latitude},{longitude}\n")


try:
    gps_file = 'gps_coordinates.txt'
    while True:
        read_and_save_gps_data(gps_file)

except KeyboardInterrupt:
    print("Keyboard interrupt. Stopping...")