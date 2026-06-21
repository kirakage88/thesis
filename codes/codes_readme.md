## Codes Reference

ESP-NOW Aircon Controller — Thesis Project

\---

### Directory Structure

```
codes/
├── prototyping/          # Integrated prototype modules (final iterations)
│   ├── ambient\_module\_final/   # Sensor module (BME280 + DS18B20 probes)
│   ├── now\_ambient\_sender/     # ESP-NOW sender (sensor data → receiver)
│   ├── now\_receiver\_supabase/  # ESP-NOW receiver + Supabase upload
│   ├── tft\_complete/           # TFT display firmware (main UI)
│   └── libraries/              # Dependencies for prototyping sketches
└── testing/             # Individual component tests \& experiments
    ├── BME280/               # BME280 sensor test
    ├── i2c\_scanner/          # I2C address scanner
    ├── mac\_address/          # ESP32 MAC address reader
    ├── now\_sender/           # ESP-NOW sender test
    ├── now\_receiver/         # ESP-NOW receiver test
    ├── now\_sender\_web/       # ESP-NOW sender + web server
    ├── now\_receiver\_web/     # ESP-NOW receiver + web server
    ├── PROBEA/               # Temperature probe A calibration
    ├── PROBEB/               # Temperature probe B calibration
    ├── PROBEC/               # Temperature probe C calibration
    ├── probes/               # Multi-probe DS18B20 test
    ├── supabase/             # Supabase insert test
    ├── tft\_custom\_fonts/     # VLW font rendering test
    ├── tft\_display/          # TFT display init \& basic drawing
    ├── tft\_gemini/           # TFT UI experiment (Gemini-assisted)
    ├── tft\_image/            # Image rendering test (pushImage)
    ├── tft\_touch/            # Touch input test
    ├── tft\_ui\_demo/          # Full UI demo (sidebar dashboard)
    ├── web\_server/           # Async web server test
    └── libraries/            # Dependencies for testing sketches
```

\---

### Prototyping

#### ambient\_module\_final/

**Purpose:** Reads ambient temperature/humidity (BME280) and three DS18B20
probe temperatures, applies calibration, outputs to Serial.

**Sensors:**

* BME280 (I2C addr `0x76`) — ambient temp + humidity
* 3× DS18B20 (OneWire bus on GPIO10) — probe temperatures

**Calibration:**

* BME280 temp: `CAL\_FACTOR = 1.0294412` (no intercept)
* BME280 hum: `Hum\_Factor = 1.0579399` (no intercept)
* Probe A: `1.701471 + 0.984997 × raw`
* Probe B/C: `1.637417 + 0.9783362 × raw`

**Libraries:** `OneWire`, `DallasTemperature`, `Adafruit\_BME280`,
`Adafruit\_Sensor`, `Wire`

\---

#### now\_ambient\_sender/

**Purpose:** Reads all sensors (same as ambient\_module\_final) and transmits
data via ESP-NOW to a receiver ESP32.

**Data struct (`EspNowData`):**

|Field|Type|Description|
|-|-|-|
|`temp`|`float`|Calibrated BME280 temp|
|`humid`|`float`|Calibrated BME280 humidity|
|`counter`|`int`|Message counter|
|`a\_temp`|`float`|Calibrated probe A temp|
|`b\_temp`|`float`|Calibrated probe B temp|
|`c\_temp`|`float`|Calibrated probe C temp|

**Config:**

* WiFi STA mode, scans for SSID to match channel
* ESP-NOW peer: receiver MAC `14:63:93:8C:FC:78`, channel 11
* Send interval: 3 seconds
* Send callback logs success/failure

**Libraries:** `WiFi`, `esp\_now`, `esp\_wire`, `Wire`,
`Adafruit\_BME280`, `OneWire`, `DallasTemperature`

\---

#### now\_receiver\_supabase/

**Purpose:** Receives ESP-NOW data from sender, uploads to Supabase
(`readings` table).

**Flow:**

1. Connects to WiFi (SSID: `PLDTHOMEFIBRd2228`)
2. Initializes Supabase client
3. Registers ESP-NOW receive callback (stores data, sets flag)
4. On `newDataReady` flag → calls `postToSupabase()`

**Supabase:**

* Table: `readings`
* Columns: `temperature`, `humidity`, `counter`, `a\_temp`, `b\_temp`, `c\_temp`
* Inserts as JSON string via `supabase.insert()`

**Safety:** Callback only sets a flag; actual HTTP POST runs in `loop()`
context (not ISR), preventing WiFi/HTTP crashes.

**Libraries:** `WiFi`, `esp\_now`, `ESPSupabase`

\---

#### tft\_complete/

**Purpose:** TFT display firmware — main UI for the aircon controller.
Currently implements the initialization/wifi screen.

**Files:**

|File|Description|
|-|-|
|`tft\_complete.ino`|Main sketch — setup, loop, pages|
|`helper\_functions.h`|Shared drawing helpers (extern `tft`)|
|`helper\_functions.cpp`|Implementation of helpers|
|`assets/wifi.h`|WiFi icon (RGB565 PROGMEM array)|
|`fonts/loraSemiBold24.h`|Lora SemiBold 24 (VLW)|
|`fonts/montserratLight13.h`|Montserrat Light 13 (VLW)|
|`fonts/montserratRegular13.h`|Montserrat Regular 13 (VLW)|

**Helper functions:**

|Function|Description|
|-|-|
|`printHeading1(text, x, y, color)`|Renders H1 text (Lora SemiBold 24)|
|`printBody(text, x, y, color)`|Renders body text (Montserrat Light 13)|
|`drawImageCenter(cx, cy, w, h, data, transparent)`|Centers and pushes an image|

**Color palette (defined in sketch):**

|Define|Value|Hex|Role|
|-|-|-|-|
|`CL\_TEXT`|`0x2104`|`#1f1f1f`|Light text|
|`CL\_SURFACE`|`0xF7BE`|`#f8f8f8`|Light bg|
|`CL\_PRIMARY`|`0x31A6`|`#333333`|Light primary|
|`CL\_SECONDARY`|`0xCE59`|`#b8b8b8`|Light secondary|
|`CL\_ACCENT`|`0x424A`|`#3f4850`|Light accent|
|`CD\_TEXT`|`0xDEFB`|`#e0e0e0`|Dark text|
|`CD\_SURFACE`|`0x0841`|`#080808`|Dark bg|
|`CD\_PRIMARY`|`0xCE59`|`#cccccc`|Dark primary|
|`CD\_SECONDARY`|`0x31A6`|`#333333`|Dark secondary|
|`CD\_ACCENT`|`0xADB7`|`#afb8c0`|Dark accent|

**Current page:** `wifiInit()` — dark rounded rect background, centered
WiFi icon, "Initializing" heading, "Wifi Station" subtext.

**Libraries:** `TFT\_eSPI`

\---

### Testing

Individual sketches for validating components in isolation. All under
`testing/` with their own `libraries/` folder.

#### Sensor Tests

|Sketch|Purpose|
|-|-|
|`BME280/`|Reads BME280 temp/humidity with calibration, outputs to Serial|
|`probes/`|Reads multiple DS18B20 probes via OneWire|
|`PROBEA/`|Probe A calibration (linear regression)|
|`PROBEB/`|Probe B calibration|
|`PROBEC/`|Probe C calibration|
|`i2c\_scanner/`|Scans I2C bus, prints device addresses|

#### ESP-NOW Tests

|Sketch|Purpose|
|-|-|
|`now\_sender/`|Basic ESP-NOW sender test|
|`now\_receiver/`|Basic ESP-NOW receiver test|
|`now\_sender\_web/`|ESP-NOW sender + async web server|
|`now\_receiver\_web/`|ESP-NOW receiver + async web server|

#### TFT Tests

|Sketch|Purpose|
|-|-|
|`tft\_display/`|Display init, basic shapes \& text|
|`tft\_custom\_fonts/`|VLW font loading/rendering test|
|`tft\_image/`|Image rendering via `pushImage()`|
|`tft\_touch/`|Touch input (XPT2046) test|
|`tft\_ui\_demo/`|Full dashboard UI demo (sidebar, cards, chart, feed)|
|`tft\_gemini/`|Gemini-assisted UI experiment|

#### Other Tests

|Sketch|Purpose|
|-|-|
|`mac\_address/`|Prints ESP32 MAC address|
|`supabase/`|Supabase insert test|
|`web\_server/`|Async web server test|

\---

### Libraries

Both `prototyping/libraries/` and `testing/libraries/` contain the same
core set:

|Library|Purpose|
|-|-|
|`TFT\_eSPI`|TFT display driver (ST7789/ILI9341)|
|`TFT\_eWidget`|UI widgets for TFT\_eSPI|
|`Adafruit\_BME280`|BME280 sensor driver|
|`Adafruit\_GFX`|Graphics primitives|
|`Adafruit\_ILI9341`|ILI9341 display driver|
|`Adafruit\_SH110X`|OLED display driver|
|`Adafruit\_TouchScreen`|Resistive touch driver|
|`Adafruit\_STMPE610`|SPI touch controller|
|`Adafruit\_TSC2007`|I2C touch controller|
|`XPT2046\_Touchscreen`|XPT2046 touch driver|
|`OneWire`|OneWire bus protocol|
|`DallasTemperature`|DS18B20 driver|
|`DHT\_sensor\_library`|DHT sensor driver|
|`ESPSupabase`|Supabase REST client for ESP32|
|`ESP\_Async\_WebServer`|Async HTTP server|
|`Async\_TCP`|Async TCP for ESP32|
|`WebSockets`|WebSocket server/client|
|`ArduinoJson`|JSON serialization|
|`Arduino\_JSON`|Arduino JSON helper|
|`Adafruit\_BusIO`|I2C/SPI bus abstraction|
|`Adafruit\_Unified\_Sensor`|Sensor abstraction layer|

\---

### Notes

* All sketches target **ESP32** (Arduino framework)
* TFT display: **ST7789 240×320** via SPI
* Touch: **XPT2046** via SPI (shared CLK with TFT)
* Fonts: VLW format, stored in PROGMEM as `.h` arrays
* Images: RGB565 arrays in PROGMEM, no runtime decoder
* ESP-NOW data struct must match exactly between sender and receiver
* Supabase receiver uses flag-based ISR safety (no HTTP in callback)

---

## Python ML Environment

The `python/machine learning/` directory contains the ML classification
experiments (Perceptron, Logistic Regression, SVM, Decision Tree, Random
Forest, KNN). These run on your local machine, not on ESP32.

### Prerequisites

- Python 3.11+ (3.14 recommended)
- `pip` (bundled with Python)
- Git (for version control)

### Virtual Environment Setup

```bash
# Navigate to the ML directory
cd "/d/School/1 Projects/thesis/codes/python/machine learning"

# Create virtual environment
python -m venv .venv

# Activate it
# PowerShell:
.venv\Scripts\Activate.ps1
# Git Bash / MSYS:
source .venv/Scripts/activate

# Install dependencies
pip install numpy matplotlib scikit-learn pandas

# Verify
python -c "import numpy, matplotlib, sklearn, pandas; print('All OK')"
```

### Dependencies

| Package | Purpose | Used In |
|---------|---------|---------|
| `numpy` | Numerical arrays | All scripts |
| `matplotlib` | Plotting decision regions | All scripts, `helper.py` |
| `scikit-learn` | ML models, datasets, metrics, preprocessing | All scripts |
| `pandas` | Data loading / preprocessing | `pre-processing/` |

### PyTorch (optional — only if you add deep learning experiments)

```bash
# CPU-only (default PyPI)
pip install torch

# CUDA 13.0 (NVIDIA GPU)
pip install torch --index-url https://download.pytorch.org/whl/cu130
```

Verify CUDA:
```python
import torch
print(torch.cuda.is_available())   # True if GPU detected
print(torch.version.cuda)           # e.g. 13.0
```

### Project Structure

```
machine learning/
├── .venv/                    # Virtual environment (git-ignored)
├── .gitignore
├── helper.py                 # plot_decision_regions() shared utility
├── 0 perceptron.py
├── 1 logistic_regression.py
├── 2 SVM.py
├── 3 dec_tree.py
├── 4 random_forest.py
├── 5 knn_classifier.py
└── pre-processing/
    ├── 6 missing values.py
    ├── 7 handling_categorical.py
    └── 8 feature_extraction
```

### .gitignore

Make sure `.gitignore` includes:

```
.venv/
__pycache__/
*.pyc
```

### VS Code Setup

1. Open the `machine learning/` folder in VS Code
2. `Ctrl+Shift+P` → "Python: Select Interpreter" → choose `.venv`
3. Terminal auto-activates the venv

