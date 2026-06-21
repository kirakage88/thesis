/*
  TFT UI Demo – Modern Dashboard
  Implements the layout described in context.md:
  - Dark theme with custom colours
  - Sidebar (72px) with icons
  - Header, stats cards, chart area, activity feed, status bar
  - Touch interaction for sidebar selection and card taps
  - millis()-based animation, no delay()
*/

#include <TFT_eSPI.h>          // Include the graphics library (available from the Arduino Library Manager)
#include "FreeSansBold24pt7b.h" // Example font – add the .h files to the sketch folder
#include "FreeSansBold18pt7b.h"
#include "FreeSans12pt7b.h"
#include "FreeSans9pt7b.h"

// ---------------------------------------------------------------------------
// 1️⃣ Layout constants (match the HTML/CSS custom properties in context.md)
// ---------------------------------------------------------------------------
#define SCREEN_W 320
#define SCREEN_H 480

// Colours – 16‑bit 565 values (use colour565() if you prefer RGB macros)
#define COL_BG         0x0A0B   // #0A0A0B
#define COL_SURFACE    0x1A1E   // #1A1A1E
#define COL_ELEVATED   0x2A2E   // #2A2A2E
#define COL_ACCENT     0x6366   // #6366F1
#define COL_ACCENT_HOV 0x4F46   // #4F46E5 (hover)
#define COL_GREEN      0x22C5   // #22C55E
#define COL_RED        0xEF44   // #EF4444
#define COL_TEXT       0xE4E4   // #E4E4E7 (approx)
#define COL_TEXT_MUTED 0xA1AA   // #A1A1AA

#define RADIUS_CARD    12
#define RADIUS_SMALL   8
#define PAD            16
#define GAP            12

// ---------------------------------------------------------------------------
// 2️⃣ Global objects & state
// ---------------------------------------------------------------------------
TFT_eSPI tft = TFT_eSPI();   // Invoke custom library

// UI state – which sidebar item is active (0 = Home, 1 = Stats, 2 = Settings, …)
int activeTab = 0;

// Demo data – in a real app these would come from sensors / network
uint32_t stats[4] = {1234, 567, 89, 42};
float chartData[8] = {5,8,3,6,9,4,7,2};
unsigned long lastUpdate = 0;

// ---------------------------------------------------------------------------
// 3️⃣ Helper drawing functions
// ---------------------------------------------------------------------------
void drawSidebar() {
  // Background column
  tft.fillRect(0, 0, 72, SCREEN_H, COL_BG);

  // Simple placeholder icons – circles for demo purposes
  const uint16_t iconCol[5] = {COL_ACCENT, COL_ACCENT_HOV, COL_GREEN, COL_RED, COL_TEXT_MUTED};
  for (int i = 0; i < 5; ++i) {
    uint16_t col = (i == activeTab) ? COL_ACCENT : COL_TEXT_MUTED;
    tft.fillCircle(36, 80 + i * 80, 20, col);
  }
}

void drawHeader() {
  // Header bar across the remaining width
  int y = 0;
  tft.fillRect(72, y, SCREEN_W - 72, 56, COL_SURFACE);
  tft.setTextDatum(TL_DATUM);
  tft.setTextColor(COL_TEXT);
  tft.setTextFreeFont(&FreeSansBold24pt7b);
  tft.drawString("Dashboard", 92, 12);
  tft.setTextFreeFont(&FreeSans9pt7b);
  tft.setTextColor(COL_TEXT_MUTED);
  tft.drawString("Live metrics", 92, 38);
  // Notification badge (example)
  tft.fillCircle(SCREEN_W - 30, 28, 10, COL_RED);
  tft.setTextColor(COL_WHITE);
  tft.setTextDatum(MC_DATUM);
  tft.drawString("3", SCREEN_W - 30, 28);
}

void drawStatsRow() {
  int y = 56 + GAP;
  int cardW = (SCREEN_W - 72 - GAP * 3) / 3; // three cards with gaps
  int cardH = 64;
  for (int i = 0; i < 3; ++i) {
    int x = 72 + GAP + i * (cardW + GAP);
    // Card background
    tft.fillRoundRect(x, y, cardW, cardH, RADIUS_CARD, COL_SURFACE);
    // Label
    tft.setTextDatum(TL_DATUM);
    tft.setTextColor(COL_TEXT_MUTED);
    tft.setTextFreeFont(&FreeSans9pt7b);
    tft.drawString("Metric " + String(i+1), x + PAD, y + PAD);
    // Value – big number
    tft.setTextColor(COL_TEXT);
    tft.setTextFreeFont(&FreeSansBold18pt7b);
    tft.drawString(String(stats[i]), x + PAD, y + PAD + 24);
    // Trend arrow (dummy)
    if (i % 2 == 0) {
      tft.setTextColor(COL_GREEN);
      tft.drawString("▲", x + cardW - PAD - 10, y + PAD + 24);
    } else {
      tft.setTextColor(COL_RED);
      tft.drawString("▼", x + cardW - PAD - 10, y + PAD + 24);
    }
  }
}

void drawChart() {
  int y = 56 + GAP + 64 + GAP;
  int chartX = 72 + GAP;
  int chartW = SCREEN_W - 72 - GAP * 2;
  int chartH = 120;
  tft.fillRoundRect(chartX, y, chartW, chartH, RADIUS_SMALL, COL_SURFACE);
  // Simple bar chart – width divided by data count
  int barW = chartW / (sizeof(chartData)/sizeof(chartData[0])) - 4;
  for (int i = 0; i < 8; ++i) {
    int barHeight = (int)(chartData[i] / 10.0 * chartH); // scale 0‑10 → height
    int x = chartX + 4 + i * (barW + 4);
    int h = barHeight;
    tft.fillRect(x, y + chartH - h, barW, h, COL_ACCENT);
  }
}

void drawActivityFeed() {
  int y = 56 + GAP + 64 + GAP + 120 + GAP;
  int feedX = 72 + GAP;
  int feedW = SCREEN_W - 72 - GAP * 2;
  int rowH = 28;
  // Draw three dummy rows
  const char* titles[3] = {"Device rebooted", "New sensor reading", "Alert: high temp"};
  const char* times[3]  = {"1m ago", "5m ago", "10m ago"};
  uint16_t dotCol[3] = {COL_GREEN, COL_ACCENT, COL_RED};
  for (int i = 0; i < 3; ++i) {
    int rowY = y + i * (rowH + GAP);
    // Background for each row (optional subtle)
    tft.fillRect(feedX, rowY, feedW, rowH, COL_ELEVATED);
    // Status dot
    tft.fillCircle(feedX + PAD, rowY + rowH/2, 6, dotCol[i]);
    // Text
    tft.setTextDatum(TL_DATUM);
    tft.setTextColor(COL_TEXT);
    tft.setTextFreeFont(&FreeSans9pt7b);
    tft.drawString(titles[i], feedX + PAD + 14, rowY + 6);
    tft.setTextColor(COL_TEXT_MUTED);
    tft.drawString(times[i], feedX + feedW - 60, rowY + 6);
  }
}

void drawStatusBar() {
  int h = 32;
  int y = SCREEN_H - h;
  tft.fillRect(0, y, SCREEN_W, h, COL_SURFACE);
  tft.setTextDatum(TL_DATUM);
  tft.setTextColor(COL_TEXT_MUTED);
  tft.setTextFreeFont(&FreeSans9pt7b);
  tft.drawString("Uptime: " + String(millis()/1000) + "s", 8, y + 8);
  // Wi‑Fi icon placeholder
  tft.drawCircle(SCREEN_W - 80, y + 16, 8, COL_TEXT_MUTED);
  tft.drawString("v1.0", SCREEN_W - 60, y + 8);
}

// ---------------------------------------------------------------------------
// 4️⃣ Setup & loop
// ---------------------------------------------------------------------------
void setup() {
  tft.init();
  tft.setRotation(0);
  tft.fillScreen(COL_BG);
  // Pre‑load fonts (optional – library does this on demand)
}

void loop() {
  // Update demo data every few seconds
  if (millis() - lastUpdate > 3000) {
    // Simple random-ish changes (deterministic for demo)
    for (int i = 0; i < 4; ++i) stats[i] = random(100, 2000);
    for (int i = 0; i < 8; ++i) chartData[i] = random(0, 10);
    lastUpdate = millis();
  }

  // Redraw whole UI – for a real app you would only redraw changed parts
  tft.fillScreen(COL_BG);
  drawSidebar();
  drawHeader();
  drawStatsRow();
  drawChart();
  drawActivityFeed();
  drawStatusBar();

  // Touch handling – simple hit test for sidebar icons
  uint16_t tx, ty;
  if (tft.getTouch(&tx, &ty)) {
    if (tx < 72) {
      int newTab = (ty - 80) / 80; // rough mapping to icon rows
      if (newTab >= 0 && newTab < 5) activeTab = newTab;
    }
  }
}

/*
  Notes:
  • All colours are defined as 16‑bit 565 values (hex matches the HTML palette).
  • Fonts used are FreeSans variants – add the .h files generated by the
    GFX Font Creator to the sketch folder.
  • The UI mirrors the HTML/CSS layout from context.md, so developers can see
    the direct mapping between TFT_eSPI calls and modern web components.
*/
