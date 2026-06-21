
#include <TFT_eSPI.h>
#include "helper_functions.h"

//Color Palette
#define CL_TEXT 0x2104
#define CL_SURFACE 0xf7be
#define CL_PRIMARY 0x31a6
#define CL_SECONDARY 0xce59
#define CL_ACCENT 0x424a

#define CD_TEXT 0xdefb
#define CD_SURFACE 0x0841
#define CD_PRIMARY 0xce59
#define CD_SECONDARY 0x31a6
#define CD_ACCENT 0xadb7



//Assets
#include "assets/wifi.h"
#define C_TRANSPARENT 0x0000

//Fonts
#include "fonts/loraSemiBold24.h"
#include "fonts/montserratLight13.h"


TFT_eSPI tft = TFT_eSPI();

//--------------------CODE HERE---------------------------//
void setup() {
  Serial.begin(115200);
  tft.init();
  tft.setRotation(2);

  wifiInit();
}

void loop() {
  // put your main code here, to run repeatedly:
}
//-------------------------------------------------------//


//--------------------PAGES HERE---------------------------//
void wifiInit(void) {
  tft.fillScreen(CL_SURFACE);
  tft.fillRoundRect(-8, -164, 256, 426, 119, CL_PRIMARY);
  drawImageCenter(120, 194, 104, 84, wifi, C_TRANSPARENT);

  printHeading1("Initializing", 54, 81, CL_SURFACE);
  printBody("Wifi Station", 83.2, 110.7, CL_SURFACE);
}


