#ifndef HELPER_FUNCTIONS_H
#define HELPER_FUNCTIONS_H

#include <TFT_eSPI.h>   

extern TFT_eSPI tft;

void printHeading1(const char* text, float x, float y, uint16_t color);
void printBody(const char* text, float x, float y, uint16_t color);
void drawImageCenter(int cx, int cy, int w, int h, const uint16_t* data, uint16_t transparent);

#endif