#include "helper_functions.h"
#include "fonts/loraSemiBold24.h"
#include "fonts/montserratLight13.h"

void printHeading1(const char* text, float x, float y, uint16_t color) {
  tft.loadFont(loraSemiBold24);
  tft.setTextColor(color);
  tft.drawString(text, x, y);
  tft.unloadFont();
}

void printBody(const char* text, float x, float y, uint16_t color) {
  tft.loadFont(montserratLight13);
  tft.setTextColor(color);
  tft.drawString(text, x, y);
  tft.unloadFont();
}

void drawImageCenter(int cx, int cy, int w, int h, const uint16_t* data, uint16_t transparent) {
  tft.pushImage(cx - w / 2, cy - h / 2, w, h, data, transparent);
}
