#include <WiFi.h>
#include <esp_now.h>
#include <esp_wifi.h>
#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BME280.h>
#include <OneWire.h>
#include <DallasTemperature.h>

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

// Replace this with your receiver ESP32 MAC address
uint8_t receiverMac[] = {0x14, 0x63, 0x93, 0x8C, 0xFC, 0x78};

const int wifiChannel = 11;

constexpr char WIFI_SSID[] = "PLDTHOMEFIBRd2228";

// Data structure must match receiver
typedef struct {
  float temp;
  float humid;
  int counter;
  float a_temp;
  float b_temp;
  float c_temp;
} EspNowData;

EspNowData dataToSend;

int counter = 0;

// Optional send callback
void onDataSent(const wifi_tx_info_t *info, esp_now_send_status_t status) {
  Serial.print("Send status: ");
  Serial.println(status == ESP_NOW_SEND_SUCCESS ? "Success" : "Failed");
}

int32_t getWiFiChannel(const char *ssid) {
  if (int32_t n = WiFi.scanNetworks()) {
      for (uint8_t i=0; i<n; i++) {
          if (!strcmp(ssid, WiFi.SSID(i).c_str())) {
              return WiFi.channel(i);
          }
      }
  }
  return 0;
}


void setup() {
  Serial.begin(115200);

  if (!bme.begin(0x76)) {
    Serial.println("Could not find a valid BME280 sensor, check wiring!");
    while (1);
  }


  WiFi.mode(WIFI_STA);

  int32_t channel = getWiFiChannel(WIFI_SSID);
  Serial.print("Channel:");
  Serial.println(channel);

  // Force sender to same channel as receiver AP
  esp_wifi_set_channel(channel, WIFI_SECOND_CHAN_NONE);

  Serial.println();
  Serial.println("Sender started");
  Serial.print("Sender MAC address: ");
  Serial.println(WiFi.macAddress());

  if (esp_now_init() != ESP_OK) {
    Serial.println("ESP-NOW initialization failed");
    return;
  }

  esp_now_register_send_cb(onDataSent);

  esp_now_peer_info_t peerInfo = {};
  memcpy(peerInfo.peer_addr, receiverMac, 6);
  peerInfo.channel = wifiChannel;
  peerInfo.encrypt = false;
  
 

  if (esp_now_add_peer(&peerInfo) != ESP_OK) {
    Serial.println("Failed to add receiver as peer");
    return;
  }

  Serial.println("Receiver peer added");
}

void loop() {
  counter++;

  // raw sensor temperature
  float temp_raw = bme.readTemperature();
  float hum_raw = bme.readHumidity();
  // calibrated temperature (no intercept model)
  float temp_calibrated = CAL_FACTOR * temp_raw;
  float hum_calibrated = Hum_Factor * hum_raw;

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


  dataToSend.temp = temp_calibrated;
  dataToSend.humid = hum_calibrated;
  dataToSend.counter = counter;
  dataToSend.a_temp = calibratedTempA;
  dataToSend.b_temp = calibratedTempB;
  dataToSend.c_temp = calibratedTempC;

  esp_err_t result = esp_now_send(receiverMac, (uint8_t *)&dataToSend, sizeof(dataToSend));

  Serial.println("");
  Serial.println("------------------");
  if (result == ESP_OK) {
    Serial.println("Data sent");
  } else {
    Serial.print("Send error: ");
    Serial.println(result);
  }
 
  Serial.println("------------------");
  Serial.println("");
  delay(3000);
  
}