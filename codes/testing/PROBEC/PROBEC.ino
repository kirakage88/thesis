#include <OneWire.h>
#include <DallasTemperature.h>

// Data wire connected to digital pin 10
#define ONE_WIRE_BUS 10

// Setup OneWire instance
OneWire oneWire(ONE_WIRE_BUS);

// Pass OneWire reference to DallasTemperature library
DallasTemperature sensors(&oneWire);

void setup(void) {
  Serial.begin(115200);
  sensors.begin();
}

void loop(void) {

  // Request temperature reading
  sensors.requestTemperatures();

  // Raw sensor temperature
  float rawTemp = sensors.getTempCByIndex(0);

  // Calibration equation from regression output
  float calibratedTemp = 1.6374170 + ( 0.9783362 * rawTemp);

  // Print raw temperature
  Serial.print("Raw Temperature: ");
  Serial.print(rawTemp);
  Serial.println(" °C");

  // Print calibrated temperature
  Serial.print("Calibrated Temperature: ");
  Serial.print(calibratedTemp);
  Serial.println(" °C");

  Serial.println("----------------------");

  delay(5000);
}