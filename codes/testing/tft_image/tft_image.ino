
#include <TFT_eSPI.h> 
#include "image.h"

TFT_eSPI tft = TFT_eSPI(); 


void setup() {
  Serial.begin(115200);
  tft.init();
  tft.setRotation(2);

  wifiInit();
}

void loop() {
  // put your main code here, to run repeatedly:

}



void wifiInit(void) {
  tft.fillScreen(0x0);
  tft.pushImage(0, 0, 240, 320, image_main_page_pixels);
}


