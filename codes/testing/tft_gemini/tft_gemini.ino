// tft_ui_demo.ino
// Required include for TFT display
#include <TFT_eSPI.h> 

TFT_eSPI tft = TFT_eSPI(); 

// --- Color Palette (RGB565 converted) ---
// Dark theme: #0A0A0B bg, #1A1A1E cards, #6366F1 accent
#define C_BG      tft.color565(10, 10, 11)     // #0A0A0B
#define C_SURFACE tft.color565(26, 26, 30)     // #1A1A1E
#define C_ELEV    tft.color565(42, 42, 46)     // #2A2A2E
#define C_ACCENT  tft.color565(99, 102, 241)   // #6366F1
#define C_TEXT    tft.color565(228, 228, 231)  // #E4E4E7
#define C_MUTED   tft.color565(161, 161, 170)  // #A1A1AA
#define C_GREEN   tft.color565(34, 197, 94)    // #22C55E
#define C_RED     tft.color565(239, 68, 68)    // #EF4444

// State variables for millis()-based updates
unsigned long lastUpdate = 0;
int activeTab = 1; 

void setup() {
  Serial.begin(115200); // Serial output for debugging
  
  tft.init();
  tft.setRotation(3); // Landscape for dashboard layout
  tft.fillScreen(C_BG);
  
  drawSidebar();
  drawDashboard();
}

void loop() {
  unsigned long currentMillis = millis();
  
  // Update UI every 1000ms without delay()
  if (currentMillis - lastUpdate >= 1000) {
    lastUpdate = currentMillis;
    updateStatusBar();
  }
  
  // Handle touch interactions
  uint16_t x, y;
  if (tft.getTouch(&x, &y)) {
    handleTouch(x, y);
  }
}

void drawSidebar() {
  // Sidebar: 72px column
  tft.fillRect(0, 0, 72, tft.height(), C_BG);
  tft.drawFastVLine(71, 0, tft.height(), C_ELEV);
  
  // Draw Tabs (Icon placeholders)
  for (int i = 0; i < 4; i++) {
    int yPos = 40 + (i * 60);
    if (i == activeTab) {
      // Active item = accent bar + filled rounded rect + highlighted icon
      tft.fillRect(0, yPos - 16, 3, 32, C_ACCENT);
      tft.fillRoundRect(8, yPos - 16, 56, 32, 8, C_SURFACE);
      tft.fillCircle(36, yPos, 8, C_ACCENT);
    } else {
      tft.fillCircle(36, yPos, 8, C_ELEV);
    }
  }
}

void drawDashboard() {
  int startX = 88;
  
  // Header: Title + Subtitle + Badge
  tft.setTextColor(C_TEXT);
  tft.setTextSize(2);
  tft.drawString("Dashboard", startX, 20);
  
  tft.setTextColor(C_MUTED);
  tft.setTextSize(1);
  tft.drawString("Overview & Stats", startX, 42);
  
  // Notification badge (red circle + number)[cite: 1]
  tft.fillCircle(startX + 130, 24, 8, C_RED);
  tft.setTextColor(TFT_WHITE);
  tft.setTextDatum(MC_DATUM);
  tft.drawString("3", startX + 130, 24);
  tft.setTextDatum(TL_DATUM); // Reset
  
  // Stats Row: rounded rect cards[cite: 1]
  for (int i = 0; i < 3; i++) {
    int cx = startX + (i * 120);
    tft.fillRoundRect(cx, 70, 110, 60, 12, C_SURFACE);
    tft.drawRoundRect(cx, 70, 110, 60, 12, C_ELEV);
    
    tft.setTextColor(C_MUTED);
    tft.drawString("Metric " + String(i+1), cx + 10, 80);
    tft.setTextColor(C_TEXT);
    tft.setTextSize(2);
    tft.drawString(String(1042 + i*23), cx + 10, 98);
    tft.setTextSize(1);
  }
  
  // Chart Area using fillRect bars and accent color[cite: 1]
  tft.fillRoundRect(startX, 145, 230, 130, 12, C_SURFACE);
  tft.drawRoundRect(startX, 145, 230, 130, 12, C_ELEV);
  tft.drawFastHLine(startX + 10, 255, 210, C_ELEV);
  for (int i = 0; i < 8; i++) {
    int barH = random(20, 90);
    tft.fillRect(startX + 20 + (i * 25), 255 - barH, 16, barH, C_ACCENT);
  }
  
  // Activity Feed: colored status dot + title + timestamp[cite: 1]
  tft.fillRoundRect(startX + 245, 145, 135, 130, 12, C_SURFACE);
  tft.drawRoundRect(startX + 245, 145, 135, 130, 12, C_ELEV);
  for (int i = 0; i < 4; i++) {
    int fy = 155 + (i * 28);
    tft.fillCircle(startX + 255, fy + 5, 4, i%2==0 ? C_GREEN : C_ACCENT);
    tft.setTextColor(C_TEXT);
    tft.drawString("Event " + String(i), startX + 265, fy);
    tft.setTextColor(C_MUTED);
    tft.drawString("1m ago", startX + 265, fy + 12);
  }
}

void updateStatusBar() {
  // Status Bar: Bottom bar — uptime + version text[cite: 1]
  tft.fillRect(72, tft.height() - 20, tft.width() - 72, 20, C_BG);
  tft.drawFastHLine(72, tft.height() - 20, tft.width() - 72, C_ELEV);
  
  tft.setTextColor(C_MUTED);
  tft.setTextDatum(ML_DATUM);
  tft.drawString("Uptime: " + String(millis() / 1000) + "s", 88, tft.height() - 10);
  
  tft.setTextDatum(MR_DATUM);
  tft.drawString("v1.0.0", tft.width() - 10, tft.height() - 10);
  tft.setTextDatum(TL_DATUM); // Reset
}

void handleTouch(uint16_t x, uint16_t y) {
  // Tap sidebar items (switch tab)[cite: 1]
  if (x < 72) {
    int clickedTab = (y - 20) / 60;
    if (clickedTab >= 0 && clickedTab < 4 && clickedTab != activeTab) {
      activeTab = clickedTab;
      drawSidebar();
      drawDashboard(); 
    }
  }
  // Tap cards (show detail)[cite: 1]
  if (x > 88 && y > 70 && y < 130) {
    Serial.println("Card clicked!");
  }
}