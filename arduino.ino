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
  if(Serial.available()){
    char c = Serial.read();
    if (c == '2')
      digitalWrite(13, HIGH);
    if (c == '3')
      digitalWrite(13, LOW);
    
    
    if (c == '1'){
      float h = dht.readHumidity();
      Serial.print("!1:H:");
      Serial.print(h);   
      Serial.print("#") ;
      
    }

    if (c == '0'){
      float t = dht.readTemperature(); 
      Serial.print("!1:T:");
      Serial.print(t);   
      Serial.print("#") ;
    }
  }
  
}
