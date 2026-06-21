// Include the libraries we need
#include <OneWire.h>
#include <DallasTemperature.h>
#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BME280.h>

#define SEALEVELPRESSURE_HPA (1013.25)

Adafruit_BME280 bme;

// calibration factor (no intercept model)
const float CAL_FACTOR = 1.0294412;
const float Hum_Factor =  1.0579399;

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

    if (!bme.begin(0x76)) {
    Serial.println("Could not find a valid BME280 sensor, check wiring!");
    while (1);
  }

}

void loop(void){ 

  // raw sensor temperature
  float temp_raw = bme.readTemperature();
  float hum_raw = bme.readHumidity();
  // calibrated temperature (no intercept model)
  float temp_calibrated = CAL_FACTOR * temp_raw;
  float hum_calibrated = Hum_Factor * hum_raw;

  Serial.println("BME280 Readings");

  Serial.print("Calibrated Temperature = ");
  Serial.print(temp_calibrated);
  Serial.println(" *C");

  Serial.print("Humidity = ");
  Serial.print(hum_calibrated);
  Serial.println(" %");

  Serial.println("------------------");



  Serial.println("Probes Temperature Readings");
  sensors.requestTemperatures(); // Send the command to get temperatures

  Serial.print("Sensor A(*C): ");
  float rawTempA = sensors.getTempC(sensorA);
  float calibratedTempA = 1.701471 + (0.984997 * rawTempA);
  Serial.println(calibratedTempA); 

 
  Serial.print("Sensor B(*C): ");
  float rawTempB = sensors.getTempC(sensorB);
  float calibratedTempB = 1.6374170 + ( 0.9783362 * rawTempB);
  Serial.println(calibratedTempB); 

  
  Serial.print("Sensor C(*C): ");
  float rawTempC = sensors.getTempC(sensorC);
  float calibratedTempC = 1.6374170 + ( 0.9783362 * rawTempC);
  Serial.println(calibratedTempC); 
  Serial.println("------------------");
  
  delay(1000);
}