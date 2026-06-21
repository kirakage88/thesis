// Include the libraries we need
#include <OneWire.h>
#include <DallasTemperature.h>

// Data wire is connected to GPIO15
#define ONE_WIRE_BUS 10
// Setup a oneWire instance to communicate with a OneWire device
OneWire oneWire(ONE_WIRE_BUS);
// Pass our oneWire reference to Dallas Temperature sensor 
DallasTemperature sensors(&oneWire);

DeviceAddress sensorC = { 0x28, 0x2A, 0x70, 0x87, 0x0, 0x9, 0x59, 0xA0 };
DeviceAddress sensorA = { 0x28, 0xD9, 0x36, 0x87, 0x0, 0xD5, 0x4E, 0xF5 };
DeviceAddress sensorB= { 0x28, 0x67, 0xCC, 0x87, 0x0, 0xA, 0x7B, 0x3B };

void setup(void){
  Serial.begin(115200);
  sensors.begin();
}

void loop(void){ 
  Serial.print("Requesting temperatures...");
  sensors.requestTemperatures(); // Send the command to get temperatures
  Serial.println("DONE");
  
  Serial.print("Sensor 1(*C): ");
  Serial.println(sensors.getTempC(sensorA)); 

 
  Serial.print("Sensor 2(*C): ");
  Serial.println(sensors.getTempC(sensorB)); 

  
  Serial.print("Sensor 3(*C): ");
  Serial.println(sensors.getTempC(sensorC)); 

  
  delay(1000);
}