#include <WiFi.h>
#include <esp_now.h>

// Shared packet structure — must match senders
typedef struct {
  uint8_t type;       // 0 = accel, 1 = ambient
  float data[6];      // payload
} EspNowPacket;

// Sender MAC addresses (add both as peers)
uint8_t accelSenderMac[]   = {0xE0, 0x72, 0xA1, 0x72, 0x22, 0x94};
uint8_t ambientSenderMac[] = {0xE0, 0x72, 0xA1, 0x72, 0x29, 0x00};

// Flag pattern for safe ISR handling
volatile bool newDataReady = false;
EspNowPacket receivedPacket;
uint8_t lastSenderMac[6];

void onDataRecv(const esp_now_recv_info_t *info, const uint8_t *data, int len) {
  if (len != sizeof(EspNowPacket)) return;

  memcpy(&receivedPacket, data, sizeof(EspNowPacket));
  memcpy(lastSenderMac, info->src_addr, 6);
  newDataReady = true;
}

void setup() {
  Serial.begin(115200);
  delay(1000);

  WiFi.mode(WIFI_STA);

  Serial.println("Receiver started");
  Serial.print("Receiver MAC: ");
  Serial.println(WiFi.macAddress());

  if (esp_now_init() != ESP_OK) {
    Serial.println("ESP-NOW init failed");
    return;
  }

  esp_now_register_recv_cb(onDataRecv);

  // Add both senders as peers
  esp_now_peer_info_t peerInfo = {};
  peerInfo.channel = 0;
  peerInfo.encrypt = false;

  memcpy(peerInfo.peer_addr, accelSenderMac, 6);
  if (esp_now_add_peer(&peerInfo) != ESP_OK) {
    Serial.println("Failed to add accel sender peer");
  }

  memcpy(peerInfo.peer_addr, ambientSenderMac, 6);
  if (esp_now_add_peer(&peerInfo) != ESP_OK) {
    Serial.println("Failed to add ambient sender peer");
  }

  Serial.println("Added accel + ambient sender peers");

  Serial.println("Listening for ESP-NOW packets...");
  Serial.println("-------------------------------");
}

void loop() {
  if (!newDataReady) return;
  newDataReady = false;

  // Print sender MAC for identification
  Serial.print("From: ");
  for (int i = 0; i < 6; i++) {
    if (i > 0) Serial.print(":");
    if (lastSenderMac[i] < 0x10) Serial.print("0");
    Serial.print(lastSenderMac[i], HEX);
  }
  Serial.print("  ");

  if (receivedPacket.type == 0) {
    // Accelerometer data
    Serial.print("Accel -> X: ");
    Serial.print(receivedPacket.data[0], 3);
    Serial.print(" Y: ");
    Serial.print(receivedPacket.data[1], 3);
    Serial.print(" Z: ");
    Serial.print(receivedPacket.data[2], 3);
    Serial.println(" m/s2");

  } else if (receivedPacket.type == 1) {
    // Ambient data
    Serial.print("Ambient -> Temp: ");
    Serial.print(receivedPacket.data[0], 2);
    Serial.print("C  Humid: ");
    Serial.print(receivedPacket.data[1], 2);
    Serial.print("%  Counter: ");
    Serial.print((int)receivedPacket.data[2]);
    Serial.print("  ProbeA: ");
    Serial.print(receivedPacket.data[3], 2);
    Serial.print("  ProbeB: ");
    Serial.print(receivedPacket.data[4], 2);
    Serial.print("  ProbeC: ");
    Serial.println(receivedPacket.data[5], 2);

  } else {
    Serial.print("Unknown type: ");
    Serial.println(receivedPacket.type);
  }
}
