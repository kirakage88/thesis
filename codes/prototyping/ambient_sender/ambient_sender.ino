#include <WiFi.h>
#include <esp_now.h>
#include <esp_wifi.h>
#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BME280.h>
#include <OneWire.h>
#include <DallasTemperature.h>

Adafruit_BME280 bme;

// Calibration factors
const float CAL_FACTOR = 1.0294412;
const float Hum_Factor = 1.0579399;

// OneWire bus
#define ONE_WIRE_BUS 10
OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature sensors(&oneWire);

DeviceAddress sensorA = {0x28, 0xD9, 0x36, 0x87, 0x0, 0xD5, 0x4E, 0xF5};
DeviceAddress sensorB = {0x28, 0x67, 0xCC, 0x87, 0x0, 0xA, 0x7B, 0x3B};
DeviceAddress sensorC = {0x28, 0x2A, 0x70, 0x87, 0x0, 0x9, 0x59, 0xA0};

// Receiver MAC address
uint8_t receiverMac[] = {0xE0, 0x72, 0xA1, 0x6F, 0xF8, 0x6C};

const int wifiChannel = 11;
constexpr char WIFI_SSID[] = "PLDTHOMEFIBRd2228";

// Shared packet structure
typedef struct {
  uint8_t type;       // 0 = accel, 1 = ambient
  float data[6];      // payload
} EspNowPacket;

EspNowPacket packet;
int counter = 0;

void onDataSent(const wifi_tx_info_t *info, esp_now_send_status_t status) {
  Serial.print("Send: ");
  Serial.println(status == ESP_NOW_SEND_SUCCESS ? "OK" : "FAIL");
}

int32_t getWiFiChannel(const char *ssid) {
  if (int32_t n = WiFi.scanNetworks()) {
    for (uint8_t i = 0; i < n; i++) {
      if (!strcmp(ssid, WiFi.SSID(i).c_str())) {
        return WiFi.channel(i);
      }
    }
  }
  return 0;
}

void setup() {
  Serial.begin(115200);
  delay(1000);

  // Init BME280
  if (!bme.begin(0x76)) {
    Serial.println("BME280 not found");
    while (1);
  }

  // Init DS18B20
  sensors.begin();

  // WiFi + ESP-NOW
  WiFi.mode(WIFI_STA);

  int32_t channel = getWiFiChannel(WIFI_SSID);
  if (channel > 0) {
    esp_wifi_set_channel(channel, WIFI_SECOND_CHAN_NONE);
    Serial.print("Channel: ");
    Serial.println(channel);
  } else {
    esp_wifi_set_channel(wifiChannel, WIFI_SECOND_CHAN_NONE);
    Serial.print("Channel fallback: ");
    Serial.println(wifiChannel);
  }

  Serial.print("Sender MAC: ");
  Serial.println(WiFi.macAddress());

  if (esp_now_init() != ESP_OK) {
    Serial.println("ESP-NOW init failed");
    return;
  }

  esp_now_register_send_cb(onDataSent);

  esp_now_peer_info_t peerInfo = {};
  memcpy(peerInfo.peer_addr, receiverMac, 6);
  peerInfo.channel = wifiChannel;
  peerInfo.encrypt = false;

  if (esp_now_add_peer(&peerInfo) != ESP_OK) {
    Serial.println("Failed to add receiver peer");
    return;
  }

  Serial.println("Receiver peer added — sending in 3s");
  delay(3000);
}

void loop() {
  counter++;

  // BME280 readings
  float temp_calibrated = CAL_FACTOR * bme.readTemperature();
  float hum_calibrated = Hum_Factor * bme.readHumidity();

  // DS18B20 readings
  sensors.requestTemperatures();
  float probeA = 1.701471 + (0.984997 * sensors.getTempC(sensorA));
  float probeB = 1.6374170 + (0.9783362 * sensors.getTempC(sensorB));
  float probeC = 1.6374170 + (0.9783362 * sensors.getTempC(sensorC));

  // Build packet
  packet.type = 1;
  packet.data[0] = temp_calibrated;
  packet.data[1] = hum_calibrated;
  packet.data[2] = (float)counter;
  packet.data[3] = probeA;
  packet.data[4] = probeB;
  packet.data[5] = probeC;

  // Local print
  Serial.print("Temp=");
  Serial.print(temp_calibrated, 2);
  Serial.print("C  Hum=");
  Serial.print(hum_calibrated, 2);
  Serial.print("%  Counter=");
  Serial.print(counter);
  Serial.print("  A=");
  Serial.print(probeA, 2);
  Serial.print("  B=");
  Serial.print(probeB, 2);
  Serial.print("  C=");
  Serial.println(probeC, 2);

  // Send
  esp_err_t result = esp_now_send(receiverMac, (uint8_t *)&packet, sizeof(packet));
  if (result != ESP_OK) {
    Serial.print("Send error: ");
    Serial.println(result);
  }

  delay(3000);
}
