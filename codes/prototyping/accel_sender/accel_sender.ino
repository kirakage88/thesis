#include <WiFi.h>
#include <esp_now.h>
#include <esp_wifi.h>
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>

Adafruit_MPU6050 mpu;

// Hardcoded calibration offsets from mpu6050_raw_20260713_152545.csv
const float AX_BIAS = -0.005124;
const float AY_BIAS = -0.265409;
const float AZ_BIAS = 0.379842;

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

  // Init MPU6050
  if (!mpu.begin()) {
    Serial.println("MPU6050 init failed");
    while (1) yield();
  }

  mpu.setAccelerometerRange(MPU6050_RANGE_4_G);
  mpu.setFilterBandwidth(MPU6050_BAND_21_HZ);

  Serial.println("MPU6050 ready");

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
  sensors_event_t a, g, temp;
  mpu.getEvent(&a, &g, &temp);

  float ax = a.acceleration.x - AX_BIAS;
  float ay = a.acceleration.y - AY_BIAS;
  float az = a.acceleration.z - AZ_BIAS;

  // Build packet
  packet.type = 0;
  packet.data[0] = ax;
  packet.data[1] = ay;
  packet.data[2] = az;
  packet.data[3] = 0;
  packet.data[4] = 0;
  packet.data[5] = 0;

  // Local print
  Serial.print("Accel: X=");
  Serial.print(ax, 3);
  Serial.print(" Y=");
  Serial.print(ay, 3);
  Serial.print(" Z=");
  Serial.print(az, 3);
  Serial.println(" m/s2");

  // Send
  esp_err_t result = esp_now_send(receiverMac, (uint8_t *)&packet, sizeof(packet));
  if (result != ESP_OK) {
    Serial.print("Send error: ");
    Serial.println(result);
  }

  delay(3000);
}
