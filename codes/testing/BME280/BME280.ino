#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BME280.h>

#define SEALEVELPRESSURE_HPA (1013.25)

Adafruit_BME280 bme;

// calibration factor (no intercept model)
const float CAL_FACTOR = 1.0294412;
const float Hum_Factor =  1.0579399;
void setup() {
  Serial.begin(9600);

  if (!bme.begin(0x76)) {
    Serial.println("Could not find a valid BME280 sensor, check wiring!");
    while (1);
  }
}

void loop() {

  // raw sensor temperature
  float temp_raw = bme.readTemperature();
  float hum_raw = bme.readHumidity();
  // calibrated temperature (no intercept model)
  float temp_calibrated = CAL_FACTOR * temp_raw;
  float hum_calibrated = Hum_Factor * hum_raw;


  Serial.print("Calibrated Temperature = ");
  Serial.print(temp_calibrated);
  Serial.println(" *C");
   
  Serial.print("Pressure = ");
  Serial.print(bme.readPressure() / 100.0F);
  Serial.println(" hPa");

  Serial.print("Approx. Altitude = ");
  Serial.print(bme.readAltitude(SEALEVELPRESSURE_HPA));
  Serial.println(" m");

  Serial.print("Humidity = ");
  Serial.print(hum_calibrated);
  Serial.println(" %");

  Serial.println();
  delay(1000);
}