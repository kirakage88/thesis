# AGENTS.md

Bachelor's thesis — Predictive Maintenance for Coiled Evaporators.
ESP32 + sensors + ESP-NOW + TFT + Supabase + scikit-learn classification.

## Firmware (Arduino / ESP32)

- All sketches target **ESP32** (Arduino framework), opened via **Arduino IDE**.
- **No build system.** Libraries live in `codes/prototyping/libraries/` and `codes/testing/libraries/` — copy or symlink into `Arduino/libraries/`.
- Serial monitor baud: **115200** (set in every sketch).

### Calibration factors (duplicated across all sensor sketches)

| Sensor | Formula |
|--------|---------|
| BME280 temp | `raw * 1.0294412` |
| BME280 humidity | `raw * 1.0579399` |
| Probe A | `1.701471 + 0.984997 * raw` |
| Probe B / C | `1.637417 + 0.9783362 * raw` |

Probe A/B/C DeviceAddress arrays hardcoded in each sketch (OneWire GPIO10).

### ESP-NOW (sender ↔ receiver)

Sender: `codes/testing/now_ambient_sender/`  |  Receiver: `codes/testing/now_receiver_supabase/`

- **Data struct must be byte-identical** between boards (`EspNowData`: `temp`, `humid`, `counter`, `a_temp`, `b_temp`, `c_temp`).
- Sender scans for SSID `PLDTHOMEFIBRd2228` to match channel before ESP-NOW init; hardcoded channel 11 as fallback.
- Receiver MAC (`0x14:63:93:8C:FC:78`) hardcoded in sender.
- Receiver WiFi credentials + Supabase URL/key hardcoded in receiver sketch.
- ESP-NOW receive callback must **only set a flag** (`volatile bool newDataReady`). HTTP POST runs in `loop()` — never in ISR.
- Supabase table: `readings`, columns: `temperature`, `humidity`, `counter`, `a_temp`, `b_temp`, `c_temp`.

### TFT display

Sketch: `codes/prototyping/tft_complete/` (ST7789 240×320, SPI)

- Touch: XPT2046 (shared SPI CLK). Full pinout in `designs/tft_display/design_readme.md` — set in TFT_eSPI `User_Setup.h`.
- **No runtime image decoder.** Convert PNG/JPG to RGB565 PROGMEM arrays (`pushImage`).
- Fonts: VLW format, stored as `.h` PROGMEM arrays in `fonts/`, loaded via `loadFont()`.
- Color palette: `#define` macros in the sketch (light/dark Iron Grey modes).

## Python ML

```
cd "codes/python/machine learning"
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r ../requirements.txt
python "0 perceptron.py"
```

- Requires **Python 3.11+**; deps pinned in `codes/python/requirements.txt` (numpy, matplotlib, scikit-learn, pandas, torch). CUDA torch is unused by current scripts.
- `helper.py` provides `plot_decision_regions()` shared by all 6 classifier scripts (0–5).
- `pre-processing/` has 3 data-wrangling scripts/dirs (`6 missing values.py`, `7 handling_categorical.py`, `8 feature_extraction`).

## Structure

```
thesis/
├── codes/
│   ├── prototyping/           # 3 final firmware sketches
│   │   ├── ambient_module_final/  # BME280 + 3×DS18B20 (sensor fusion, no wireless)
│   │   ├── mpu6050_calibration/  # MPU6050 gyro/accel bias calibration
│   │   ├── tft_complete/          # ST7789 TFT UI
│   │   └── libraries/             # Dependencies
│   ├── testing/               # 22 standalone component sketches
│   │   ├── now_ambient_sender/    # ESP-NOW sender (sensor → receiver)
│   │   ├── now_receiver_supabase/ # ESP-NOW receiver → Supabase
│   │   ├── now_sender/ now_receiver/ now_sender_web/ now_receiver_web/
│   │   ├── BME280/ probes/ PROBEA/ PROBEB/ PROBEC/
│   │   ├── tft_display/ tft_touch/ tft_custom_fonts/ tft_image/ tft_ui_demo/ tft_gemini/
│   │   ├── supabase/ web_server/ mac_address/ i2c_scanner/ mpu6050/
│   │   └── libraries/
│   └── python/
│       ├── machine learning/  # 6 classifiers + pre-processing/
│       └── deep learning/     # empty
├── designs/  # TFT mockups, VLW fonts, palette, logos
└── schematics/  # Fritzing .fzz files
```

## What is NOT here

- CI/CD, linters, formatters, type checkers, test frameworks.
- Root `.gitignore` (only `codes/python/machine learning/.gitignore` exists).
- Package manager config at repo root.
