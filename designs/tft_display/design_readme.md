## TFT Display Design Reference

ESP-NOW Aircon Controller — Thesis Project





\---

### Design Direction

Modern, minimal, abstract. Clean typography, generous whitespace, no
decorative clutter. Content-first layout with a restrained color palette.

Inspiration: [Realtime Colors](https://www.realtimecolors.com/?colors=1f1f1f-f7f7f7-333333-adadad-3f4850&fonts=Lora-Montserrat)
(Lora + Montserrat font pair), [M3 Material](https://m3.material.io/).

\---





### Color Palette — Iron Grey (RGB565)

Defined as `#define` macros in a shared `colors.h` (zero RAM, no duplication).





#### Core Defines (colors.h)

|Name|Hex|RGB565|Role|
|-|-|-|-|
|`COL\\\\\\\_BRIGHT\\\\\\\_SNOW`|`#f8f8f8`|`0xFFDF`|Background / text on dark|
|`COL\\\\\\\_SILVER`|`#cccccc`|`0xCE79`|Borders, dividers|
|`COL\\\\\\\_SILVER\\\\\\\_2`|`#aeaeae`|`0xAD75`|Disabled states|
|`COL\\\\\\\_IRON\\\\\\\_GREY`|`#474747`|`0x4228`|Primary text, dark bgs|
|`COL\\\\\\\_IRON\\\\\\\_GREY\\\\\\\_2`|`#4b5660`|`0x4AAC`|Accent, headers|

#### 

#### 

#### Light Mode

|Name|Hex|RGB565|Role|
|-|-|-|-|
|Carbon Black|`#1f1f1f`|`0x2104`|Text|
|Bright Snow|`#f8f8f8`|`0xF7BE`|Surface|
|Graphite|`#333333`|`0x31A6`|Primary|
|Silver|`#b8b8b8`|`0xCE59`|Secondary|
|Alabaster Grey|`#ebebeb`|—|Surface Container|
|Charcoal Blue|`#3f4850`|`0x424A`|Accent|

#### 

#### 

#### Dark Mode

|Name|Hex|RGB565|Role|
|-|-|-|-|
|Carbon Black|`#e0e0e0`|`0xDEFB`|Text|
|Bright Snow|`#080808`|`0x0841`|Surface|
|Graphite|`#cccccc`|`0xCE59`|Primary|
|Silver|`#333333`|`0x31A6`|Secondary|
|Charcoal Blue|`#afb8c0`|`0xADB7`|Accent|

\---





### Font Rules

All fonts are VLW, stored in PROGMEM as `.h` arrays.
Load via `loadFont()` / `unloadFont()` per screen.

|Role|Font|Size|Use|
|-|-|-|-|
|H1|Lora SemiBold|24px|Page titles, welcome heading|
|H2|Lora Regular|18px|Sub-headings, taglines|
|Emphasis|Montserrat Regular|13px|Labels, active states, button text|
|Body|Montserrat Light|13px|Descriptions, list items, secondary|

Custom fonts directory: `custom\\\\\\\_tft\\\\\\\_fonts/fontsketch/`

\---











### Navigation Model (Option B)

Mobile-app pattern: persistent bottom bar + center arrow above it
that expands a full-screen menu.

* **Bottom bar** — quick access to most-used screens (Devices, Units)
* **Center arrow** — opens full-screen menu with ALL destinations
* Bar persists on every page; active tab highlighted (accent color)
* Reserve bar height (\~40–50px): `CONTENT\\\\\\\_HEIGHT = TFT\\\\\\\_HEIGHT - BAR\\\\\\\_HEIGHT`
* No back arrow on Main Menu (it is the root)

\---









### Pages

#### 1\. Main Menu

* Logo at top center
* "Welcome" (H1) below logo
* Rotating tagline (H2) below welcome — cycles every 2–3s:

  1. "All sensors, one screen"
  2. "Monitor · Manage · Control."
  3. "Every unit, simplified"
  4. "Control every unit"
* 2×2 button grid:

|Button|Icon|Label|
|-|-|-|
|Pairing|link/wifi|Pairing|
|Devices|chip|Devices|
|Units|snowflake|Units|
|System|gear|System|

* Center arrow above bottom bar
* Persistent bottom bar

#### 2\. Pairing

* Auto-search mode + manual ESP-NOW pair
* Action buttons, dialog/popup for confirm

#### 3\. Devices List

* List view with status indicators
* Per-device send-status toggle

#### 4\. Units List

* Expand/collapse list (aircon unit → assigned ESP devices)
* Add/remove action buttons

#### 5\. System

TBD











\---

### UI Components Needed

Button grid, list view with status, expand/collapse list, toggle switch,
action buttons, dialog/popup, bottom bar, full-screen menu/drawer,
rotating tagline, logo image

\---









### Assets

Directory: `assets/`

|File|Format|Purpose|
|-|-|-|
|`ac.svg`|SVG|Aircon/Units icon|
|`chip.svg`|SVG|Devices icon|
|`pair.svg`|SVG|Pairing icon|
|`system.svg`|SVG|System/Settings icon|
|`wifi.png`|PNG|WiFi icon|

Icons: Material Symbols Outlined (Google Fonts), 24px, wght 400, GRAD 0.

Other design files:

|File|Purpose|
|-|-|
|`home\\\\\\\_page.png`|Main menu mockup|
|`init\\\\\\\_page.png`|Initialization page mockup|
|`palette\\\\\\\_shades.png`|Full palette shade reference|
|`pureref.pur`|PureRef design reference|
|`tft.af`|Affinity Designer file|

\---









### Shared Infrastructure

* **Screen manager** — owns active screen, dispatches touch, handles transitions
* **Custom fonts** — VLW in PROGMEM (`.h` arrays), 4 fonts loaded on demand
* **Color scheme** — single `#define` block in `colors.h`, shared across all screens
* **Helper functions** — `helper\\\\\\\_functions.h/.cpp` (shared `tft` via `extern`)
e.g. `drawImageCenter`, `drawIconCenter`, color/draw helpers

\---









### Design Decisions

* Modern, minimal, abstract — no decorative elements, content-first
* No back arrow on Main Menu (root page)
* Center arrow above bottom bar opens full-screen menu
* Icons + labels per button/tab (use `drawIconCenter`)
* Icon-only on bottom bar if width is tight (240px display)
* Rotating taglines cycle every 2–3 seconds
* Status indicator for ESP-NOW state (connected / searching / offline)
* Avoid clutter (battery %, time) unless load-bearing for demo

\---











### TFT\_eSPI Pinout

|TFT Pin|GPIO|
|-|-|
|VCC|5V|
|GND|GND|
|CS|7|
|RESET|3|
|DC|2|
|SDI (MOSI)|6|
|SCK|4|
|LED|3.3V|
|SDO (MISO)|5|
|T\_CLK|4|
|T\_CS|8|
|T\_DIN|6|
|T\_DO|5|
|T\_IRQ|—|

\---







### Notes

* TFT\_eSPI has no runtime image decoder/scaler. Convert PNG/JPG/SVG to
RGB565 (`pushImage`) or 1-bit XBM (`drawXBitmap`) arrays on PC first.
* Display: ST7789 240×320 via SPI
* Touch: XPT2046 via SPI (shared CLK with TFT)

