#include <esp_now.h>
#include <WiFi.h>
#include "ESPAsyncWebServer.h"
#include <Arduino_JSON.h>

// Access point settings
const char* ssid = "PLDTHOMEFIBRd2228";
const char* password = "PLDTWIFIkydr9";

AsyncWebServer server(80);

// Data structure must match sender
typedef struct {
  float temp;
  float humid;
  int counter;
} EspNowData;

EspNowData latestData;

bool dataReceived = false;

// ESP-NOW receive callback
void onDataReceived(const esp_now_recv_info_t *info, const uint8_t *incomingData, int len) {
  memcpy(&latestData, incomingData, sizeof(latestData));
  dataReceived = true;

  Serial.println("Data received:");
  Serial.print("Temperature: ");
  Serial.println(latestData.temp);
  Serial.print("Humidity: ");
  Serial.println(latestData.humid);
  Serial.print("ReadingID: ");
  Serial.println(latestData.counter);
  Serial.println();
}

// Creates JSON data for the webpage
String getJsonData() {
  JSONVar data;

  data["received"] = dataReceived;
  data["temp"] = latestData.temp;
  data["humid"] = latestData.humid;
  data["counter"] = latestData.counter;

  return JSON.stringify(data);
}

// HTML page stored in program memory
const char index_html[] PROGMEM = R"rawliteral(
<!DOCTYPE HTML>
<html>
<head>
  <meta charset="UTF-8">  
  <title>BME280 ESP-NOW DASHBOARD</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.7.2/css/all.css">
  <link rel="icon" href="data:,">

  <style>
    html { font-family: Arial; text-align: center; }
    body { margin: 0; }
    .topnav { background-color: #2f4468; color: white; font-size: 1.7rem; padding: 10px; }

    .content { padding: 20px; }

    .cards {
      max-width: 500px;
      margin: 0 auto;
      display: grid;
      grid-gap: 20px;
      grid-template-columns: 1fr;
    }

    .card {
      background: white;
      box-shadow: 2px 2px 12px rgba(140,140,140,.5);
      padding: 20px;
      border-radius: 10px;
    }

    .reading { font-size: 2.5rem; }

    .id { font-size: 1rem; color:grey;}

    .temperature { color: #fd7e14; }
    .humidity { color: #1b78e2; }
  </style>
</head>

<body>

  <div class="topnav">
    <h3>BME280 ESP-NOW DASHBOARD</h3>
  </div>

  <div class="content">
    <div class="cards">

      <!-- TEMPERATURE -->
      <div class="card temperature">
        <h4><i class="fas fa-thermometer-half"></i> TEMPERATURE</h4>
        <p class="reading"><span id="temperature">--</span> °C</p>
      </div>

      <!-- HUMIDITY -->
      <div class="card humidity">
        <h4><i class="fas fa-tint"></i> HUMIDITY</h4>
        <p class="reading"><span id="humidity">--</span> %</p>
      </div>

      <p class="id">Reading ID: <span id="readingID">--</span></p>
      <p class="id" id="status">Waiting for data...</p>

    </div>
  </div>

  <script>  
    async function updateData() {
      try { 
        const response = await fetch('/data');
        const data = await response.json();

        document.getElementById('temperature').textContent = Number(data.temp).toFixed(2);
        document.getElementById('humidity').textContent = Number(data.humid).toFixed(2);
        document.getElementById('readingID').textContent = data.counter;

        document.getElementById('status').textContent = data.received
          ? 'Receiving ESP-NOW data'
          : 'No ESP-NOW data received yet';
      } catch (error) {
        document.getElementById('status').textContent = 'Website connection error';
      }
    }

    updateData();
    setInterval(updateData, 1000);
  </script>
</body>
</html>
)rawliteral";

void setup() {
  Serial.begin(115200);

  latestData.temp = 0.0;
  latestData.humid = 0.0;
  latestData.counter = 0;

  WiFi.mode(WIFI_STA);


  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
  delay(500);
  Serial.print(".");
  }

  Serial.println();
  Serial.println("WiFi connected");
  Serial.print("Receiver IP address: ");
  Serial.println(WiFi.localIP());
  Serial.print("WiFi channel: ");
  Serial.println(WiFi.channel());
  Serial.print("Receiver MAC address: ");
  Serial.println(WiFi.macAddress());

  if (esp_now_init() != ESP_OK) {
    Serial.println("ESP-NOW initialization failed");
    return;
  }

  esp_now_register_recv_cb(onDataReceived);

  server.on("/", HTTP_GET, [](AsyncWebServerRequest *request) {
    request->send_P(200, "text/html", index_html);
  });

  server.on("/data", HTTP_GET, [](AsyncWebServerRequest *request) {
    request->send(200, "application/json", getJsonData());
  });

  server.begin();

  Serial.println("Async web server started");
}

void loop() {
  // Nothing needed here.
  // ESPAsyncWebServer handles clients in the background.
  // ESP-NOW receive callback also runs automatically.
}