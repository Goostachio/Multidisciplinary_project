#include "DHT.h" 
const int DHTPIN = 4;      
const int DHTTYPE = DHT11;  
DHT dht(DHTPIN, DHTTYPE); 
void setup() {
  // put your setup code here, to run once:
  pinMode(13, OUTPUT);
  Serial.begin(115200);
  dht.begin();
}

void loop() {
  if(Serial.available()){  // Check if there is data available in the Serial buffer
    char c = Serial.read();  // Read a single character from the Serial buffer
    
    // If the received character is '1'
    if (c == '1'){  
      // Read the humidity value from the DHT sensor and convert it to float value
      float h = dht.readHumidity();
      Serial.print("!1:H:");   // Send a header indicating humidity data
      Serial.print(h);   // Send the humidity value
      Serial.print("#"); // Send a footer to mark the end of the data
      
      // the printed data is going to look something like this "!1:H:78#"
      
    }

    // If the received character is '0'
    if (c == '0'){
      float t = dht.readTemperature(); // Read the temperature value from the DHT sensor
      Serial.print("!1:T:"); // Send a header indicating temperature data
      Serial.print(t);  // Send the temperature value
      Serial.print("#") ; // Send a footer to mark the end of the data

      // the printed data is going to look something like this "!1:T:31#"

    }
  }
  
}
