# AGENTS.md

Bachelor's thesis — Predictive Maintenance for Coiled Evaporators.
ESP32 + sensors + ESP-NOW + TFT + Supabase + scikit-learn classification.

## Repo layout

```
thesis/
├── codes/
│   ├── prototyping/           # Final integrated firmware (4 sketches)
│   │   ├── ambient_module_final/     # BME280 + 3×DS18B20 sensor fusion
│   │   ├── now_ambient_sender/       # Sensor + ESP-NOW transmitter
│   │   ├── now_receiver_supabase/    # ESP-NOW receiver → Supabase INSERT
│   │   └── tft_complete/             # ST7789 TFT UI (main display)
│   ├── testing/               # 18 standalone component sketches
│   └── python/
│       └── machine learning/  # 6 classifier scripts + pre-processing/
├── designs/  # TFT mockups, VLW fonts, palette, logos
├── schematics/  # Fritzing .fzz files
└── resources/  # Reference PDFs (git-ignored)
```

## Firmware (Arduino / ESP32)

- All sketches target **ESP32** (Arduino framework), opened via **Arduino IDE**.
- **No build system** (no platformio.ini at repo root). Libraries live in `prototyping/libraries/` and `testing/libraries/` — copy or symlink into `Arduino/libraries/`.
- Serial monitor baud: **115200** (set in every sketch).
- Required libraries: `TFT_eSPI`, `OneWire`, `DallasTemperature`, `Adafruit_BME280`, `ESPSupabase`, `ArduinoJson` (see `codes_readme.md` for full list).
- TFT pinout defined in `designs/tft_display/design_readme.md` — set in `User_Setup.h` of TFT_eSPI.

### ESP-NOW critical details

- **Data struct must be identical** between sender and receiver (`EspNowData` with fields: `temp`, `humid`, `counter`, `a_temp`, `b_temp`, `c_temp`).
- Sender MAC (`0x14:63:93:8C:FC:78`) and channel (11) hardcoded in `now_ambient_sender/`.
- Receiver WiFi credentials, Supabase URL/key hardcoded in `now_receiver_supabase/`.
- ESP-NOW callback must **only set a flag** (`volatile bool newDataReady`); HTTP POST to Supabase runs in `loop()` to avoid crashes.
- Sender scans for the target SSID to match WiFi channel before ESP-NOW init.

### Calibration factors (duplicated across sketches)

| Sensor | Formula |
|--------|---------|
| BME280 temp | `raw * 1.0294412` |
| BME280 humidity | `raw * 1.0579399` |
| Probe A | `1.701471 + 0.984997 * raw` |
| Probe B / C | `1.637417 + 0.9783362 * raw` |

### TFT display

- **ST7789 240×320**, SPI. Touch: **XPT2046** (shared SPI CLK).
- **No runtime image decoder** — convert PNG/JPG to RGB565 PROGMEM arrays (`pushImage`) offline.
- Fonts: VLW format, stored as `.h` PROGMEM arrays in `fonts/`, loaded via `loadFont()`.
- Color palette: Iron Grey (light/dark mode) — `#define` macros in sketch.

## Python ML

```
cd "codes/python/machine learning"
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r ../requirements.txt
python "0 perceptron.py"
```

- Requires **Python 3.11+** with `numpy`, `matplotlib`, `scikit-learn`, `pandas`.
- `helper.py` provides `plot_decision_regions()` shared by all classifier scripts.
- Scripts 0–5 are standalone classifiers; `pre-processing/` has data wrangling scripts.
- CUDA variants in requirements (`torch==2.12`) are optional (unused by current scripts).

## What this repo does NOT have

- CI/CD workflows, linters, formatters, type checkers, or test frameworks.
- Root `.gitignore` (only `codes/python/machine learning/.gitignore` ignores `.venv/`, `__pycache__/`).
- Package manager config at repo root.
- The `codes/website/` directory is empty.
- `codes/python/deep learning/` directory exists but is empty.
