#include <SPI.h>
#include <TFT_eSPI.h>
#include <XPT2046_Touchscreen.h>

// ESP32-C3 Standard SPI Pins
#define SPI_SCK  4
#define SPI_MISO 5
#define SPI_MOSI 6

// Your specific touch pins
#define XPT2046_CS   8 
//#define XPT2046_IRQ  2  

TFT_eSPI tft = TFT_eSPI();
XPT2046_Touchscreen touchscreen(XPT2046_CS);

#define SCREEN_WIDTH 320
#define SCREEN_HEIGHT 240
#define FONT_SIZE 2

// Touchscreen coordinates: (x, y) and pressure (z)
int x, y, z;

// Print Touchscreen info about X, Y and Pressure (Z) on the Serial Monitor
void printTouchToSerial(int touchX, int touchY, int touchZ) {
  Serial.print("X = ");
  Serial.print(touchX);
  Serial.print(" | Y = ");
  Serial.print(touchY);
  Serial.print(" | Pressure = ");
  Serial.print(touchZ);
  Serial.println();
}

// Print Touchscreen info about X, Y and Pressure (Z) on the TFT Display
void printTouchToDisplay(int touchX, int touchY, int touchZ) {
  // Clear TFT screen
  tft.fillScreen(TFT_WHITE);
  tft.setTextColor(TFT_BLACK, TFT_WHITE);

  int centerX = SCREEN_WIDTH / 2;
  int textY = 80;
 
  String tempText = "X = " + String(touchX);
  tft.drawCentreString(tempText, centerX, textY, FONT_SIZE);

  textY += 20;
  tempText = "Y = " + String(touchY);
  tft.drawCentreString(tempText, centerX, textY, FONT_SIZE);

  textY += 20;
  tempText = "Pressure = " + String(touchZ);
  tft.drawCentreString(tempText, centerX, textY, FONT_SIZE);
}

void setup() {
  Serial.begin(115200);

  // Force the global SPI bus to use the C3's pins (SCK, MISO, MOSI, CS)
  SPI.begin(SPI_SCK, SPI_MISO, SPI_MOSI, -1);

  // Start the touchscreen using the shared global SPI
  touchscreen.begin();
  touchscreen.setRotation(1);

  // Start the tft display
  tft.init();
  tft.setRotation(1);

  // Clear the screen before writing to it
  tft.fillScreen(TFT_WHITE);
  tft.setTextColor(TFT_BLACK, TFT_WHITE);
  
  // Set X and Y coordinates for center of display
  int centerX = SCREEN_WIDTH / 2;
  int centerY = SCREEN_HEIGHT / 2;

  tft.drawCentreString("Hello, ESP32-C3!", centerX, 30, FONT_SIZE);
  tft.drawCentreString("Touch screen to test", centerX, centerY, FONT_SIZE);
}

void loop() {
  // Checks if Touchscreen was touched (uses the IRQ pin for efficiency)
  if (touchscreen.tirqTouched() && touchscreen.touched()) {
    
    // Get raw Touchscreen points
    TS_Point p = touchscreen.getPoint();
    
    // Calibrate Touchscreen points with map function to screen resolution
    x = map(p.x, 200, 3700, 1, SCREEN_WIDTH);
    y = map(p.y, 240, 3800, 1, SCREEN_HEIGHT);
    z = p.z;

    printTouchToSerial(x, y, z);
    printTouchToDisplay(x, y, z);

    delay(100);
  }
}