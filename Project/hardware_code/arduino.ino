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
  // Check if there is data available in the Serial buffer
  if(Serial.available()){
    // Read a single character from the Serial buffer  
    char c = Serial.read();  
    
    // If the received character is '1'
    if (c == '1'){  
      /*Read the humidity value from the DHT sensor
      and convert it to float value*/ 
      float h = dht.readHumidity();
      // Send a header indicating humidity data
      Serial.print("!1:H:");  
      // Send the humidity value
      Serial.print(h);   
      // Send a footer to mark the end of the data
      Serial.print("#"); 
      
// the printed data is going to look something like this "!1:H:78#"
      
    }

    // If the received character is '0'
    if (c == '0'){
      // Read the temperature value from the DHT sensor
      float t = dht.readTemperature(); 
      // Send a header indicating temperature data
      Serial.print("!1:T:"); 
      // Send the temperature value
      Serial.print(t);
      // Send a footer to mark the end of the data  
      Serial.print("#") ; 

// the printed data is going to look something like this "!1:T:31#"

    }
  }
  
}
