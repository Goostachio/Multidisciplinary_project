import serial
import sensor

# Define the serial port and baud rate to match the Arduino source sode
SERIAL_PORT = sensor.get_port()  # Find connected port name in the system
BAUD_RATE = 9600 

# A function to read data from port
def read_gps_data(sim_latitude, sim_longitude):
    # The parameters this function takes is for a simulated gps coordinates that is stored in a text file
    # In the case that the serial port is accessed, it will read from the port as below
    
    try:
        # Open the serial port and set the baud rate and timeout
        with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1) as ser: 
            
            # Continuously read data from the serial port
            while True:

                # Read a line of text from the serial port and decode it to a string
                line = ser.readline().decode('utf-8').strip() 

                # Check if the line contains GPS coordinate data in the format "Latitude= ... Longitude= ..."
                if line.startswith("Latitude= ") and line.count(" Longitude= ") == 1:

                    # Split the line into three parts based on whitespace characters
                    _, lat_str, lon_str = line.split()

                    # Convert the latitude and longitude strings to floating-point numbers 
                    # for distance calculations in the main source code
                    latitude = float(lat_str)
                    longitude = float(lon_str)

                    #return the processed coordinates
                    return latitude, longitude
                
    # In the case that the serial port is not accessible, this function returns coordinate values from paramater         
    except serial.SerialException:
        return sim_latitude, sim_longitude



