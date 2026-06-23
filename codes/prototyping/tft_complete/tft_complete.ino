
#include <TFT_eSPI.h>
#include "helper_functions.h"

//Color Palette
#define CL_TEXT 0x2104
#define CL_ACCENT 0x424a
#define CL_PRIMARY 0x31a6
#define CL_SECONDARY 0xce59
#define CL_CONTAINER 0xdefb
#define CL_SURFACE 0xf7be


#define CD_TEXT 0xdefb
#define CD_SURFACE 0x0841
#define CD_PRIMARY 0xce59
#define CD_SECONDARY 0x31a6
#define CD_ACCENT 0xadb7



//Assets
#include "assets/wifi.h"
#include "assets/home.h"
#include "assets/nav_container.h"

#include "assets/pair.h"
#include "assets/devices.h"
#include "assets/units.h"
#include "assets/system_info.h"

#include "assets/en_pair.h"
#include "assets/en_devices.h"
#include "assets/en_units.h"
#include "assets/en_system_info.h"
//#include "assets/home_page.h" //Debug
#define C_TRANSPARENT 0x0000

//Fonts
#include "fonts/loraSemiBold24.h"
#include "fonts/montserratLight13.h"


TFT_eSPI tft = TFT_eSPI();


struct NavIcon {
    const uint16_t* bmp;
    uint16_t x, y, w, h;
};

const NavIcon nav_icons[4][2] = {
    // icon 0: pair
    { { pair,      29, 280, 24, 34 },
      { en_pair,   22, 280, 40, 33 } },
    // icon 1: devices
    { { devices,   74, 280, 38, 34 },
      { en_devices,74, 280, 40, 33 } },
    // icon 2: units
    { { units,     133, 280, 25, 33 },
      { en_units,  126, 280, 40, 33 } },
    // icon 3: system_info
    { { system_info,   180, 280, 35, 35 },
      { en_system_info, 178, 280, 40, 35 } },
};


int nav_selected = 0;
unsigned long last_switch = 0;


//--------------------CODE HERE---------------------------//
void setup() {
  Serial.begin(115200);
  tft.init();
  tft.setRotation(2);


}

void loop() {

  if (millis() - last_switch >= 1000) {
    last_switch = millis();
    nav_selected++;
    if (nav_selected > 4) nav_selected = 0;
    homePage();
  }
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


void homePage(void) {
  //Background
  tft.pushImage(0, 0, 240, 320, home);


  //Navigation Bar
  tft.pushImage(4, 275, 232, 42, nav_container, C_TRANSPARENT);

  //tft.pushImage(0, 0, 240, 320, home_page);
  for (int i = 0; i < 4; i++) {
    int state = (nav_selected == i + 1) ? 1 : 0;
    const NavIcon& icon = nav_icons[i][state];
    tft.pushImage(icon.x, icon.y, icon.w, icon.h, icon.bmp, C_TRANSPARENT);
  }
}
