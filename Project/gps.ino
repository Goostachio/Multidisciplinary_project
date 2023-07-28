#include <TinyGPS++.h>
#include <SoftwareSerial.h>

// Define the pins for the SoftwareSerial RX (Receive) and TX (Transmit) connections
static const int RXPin = 4, TXPin = 3;

// Define the baud rate for communication with the GPS device
static const uint32_t GPSBaud = 9600;

// The TinyGPS++ object
TinyGPSPlus gps;

// The serial connection to the GPS device
SoftwareSerial ss(RXPin, TXPin);

// Setup function, runs once when the Arduino is powered on or reset
void setup(){
  Serial.begin(9600); // Initialize the Serial communication with the computer
  ss.begin(GPSBaud); // Initialize the SoftwareSerial communication with the GPS device
}

// Loop function, runs repeatedly after the setup function
void loop(){

  // Check if there is data available in the SoftwareSerial buffer
  while (ss.available() > 0){  

    // Read a single byte of data from the SoftwareSerial buffer and feed it to the TinyGPSPlus object for decoding
    gps.encode(ss.read());

    // Check if a new GPS location has been successfully decoded and updated
    if (gps.location.isUpdated()){

      /*
      If a new GPS location is successfully decoded and updated in the gps object,
      we print the latitude and longitude values to the Serial Monitor with 6 decimal places.
      */
      Serial.print("Latitude= "); 
      Serial.print(gps.location.lat(), 6);  
      Serial.print(" Longitude= "); 
      Serial.println(gps.location.lng(), 6);

      // The output is going to look something like this: "Latitude= 11.072128 Longitude= 106.580999"
    }
  }
}


