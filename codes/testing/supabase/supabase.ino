// Import WiFi and ESPSupabase Library
#include <WiFi.h>
#include <ESPSupabase.h>

// Add you Wi-Fi credentials
const char* ssid = "PLDTHOMEFIBRd2228";
const char* password = "PLDTWIFIkydr9";

const char* SUPABASE_URL = "https://siawxhbimofcyamwjejo.supabase.co";
const char* SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InNpYXd4aGJpbW9mY3lhbXdqZWpvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODA2NjA3MTcsImV4cCI6MjA5NjIzNjcxN30.Z_pCnXrpI6CZfzlczq0zyo77TdQxKCwQXhZ9UiOyQ_o";


Supabase supabase;

void setup() {
  Serial.begin(115200);

  // Connect to Wi-Fi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to Wi-Fi...");
  }
  Serial.println("Wi-Fi connected!");

  // Init Supabase
  supabase.begin(SUPABASE_URL, SUPABASE_KEY);

  // Add the table name here

  // sending data to supabase

}

void loop() {
  String tableName = "readings";
  // change the correct columns names you create in your table
  String jsonData = "{\"temperature\": \"70\", \"humidity\": \"37\", \"counter\": \"37\"}";
  Serial.println(jsonData);
  int response = supabase.insert(tableName, jsonData, false);
  if (response == 200) {
    Serial.println("Data inserted successfully!");
  } else {
    Serial.print("Failed to insert data. HTTP response: ");
    Serial.println(response);
  }

  delay(100);
}