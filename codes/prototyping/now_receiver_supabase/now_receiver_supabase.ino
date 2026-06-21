#include <esp_now.h>
#include <WiFi.h>
#include <ESPSupabase.h>

// WiFi
const char* ssid = "PLDTHOMEFIBRd2228";
const char* password = "PLDTWIFIkydr9";

// Supabase
const char* SUPABASE_URL = "https://siawxhbimofcyamwjejo.supabase.co";
const char* SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InNpYXd4aGJpbW9mY3lhbXdqZWpvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODA2NjA3MTcsImV4cCI6MjA5NjIzNjcxN30.Z_pCnXrpI6CZfzlczq0zyo77TdQxKCwQXhZ9UiOyQ_o";
Supabase supabase;

// Data structure
typedef struct {
  float temp;
  float humid;
  int counter;
  float a_temp;
  float b_temp;
  float c_temp;
} EspNowData;

EspNowData latestData;

// IMPORTANT: control flag
volatile bool newDataReady = false;

// ESP-NOW callback (ONLY STORE DATA)
void onDataReceived(const esp_now_recv_info_t *info,
                    const uint8_t *incomingData,
                    int len) {

  memcpy(&latestData, incomingData, sizeof(latestData));

  newDataReady = true;

  Serial.println("Data Received");
}

// SAFE Supabase function (runs in loop context)
void postToSupabase() {

  String jsonData = "{";
  jsonData += "\"temperature\":\"" + String(latestData.temp) + "\",";
  jsonData += "\"humidity\":\"" + String(latestData.humid) + "\",";
  jsonData += "\"counter\":\"" + String(latestData.counter) + "\",";
  jsonData += "\"a_temp\":\"" + String(latestData.a_temp) + "\",";
  jsonData += "\"b_temp\":\"" + String(latestData.b_temp) + "\",";
  jsonData += "\"c_temp\":\"" + String(latestData.c_temp) + "\"";
  jsonData += "}";

  Serial.println("Sending to Supabase:");
  Serial.println(jsonData);

  int response = supabase.insert("readings", jsonData, false);

  Serial.print("HTTP response: ");
  Serial.println(response);

  if (response == 200 || response == 201) {
    Serial.println("Insert success");
  } else {
    Serial.println("Insert failed");
    
  }
  Serial.println();
}

void setup() {

  Serial.begin(115200);

  WiFi.mode(WIFI_STA);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("\nWiFi connected");
  Serial.println(WiFi.localIP());
  Serial.print("WiFi channel: ");
  Serial.println(WiFi.channel());
  Serial.print("Receiver MAC address: ");
  Serial.println(WiFi.macAddress());

  // Supabase init
  supabase.begin(SUPABASE_URL, SUPABASE_KEY);
  Serial.println("Supabase connected");

  // ESP-NOW init
  if (esp_now_init() != ESP_OK) {
    Serial.println("ESP-NOW init failed");
    return;
  }

  esp_now_register_recv_cb(onDataReceived);
}

void loop() {

  // ONLY here we talk to Supabase
  if (newDataReady) {

    newDataReady = false;

    delay(100); // small buffer time for stability

    postToSupabase();
  }
}