# AGENTS.md

Bachelor's thesis — Predictive Maintenance for Coiled Evaporators.
ESP32 + sensors + ESP-NOW + TFT + Supabase + ML classification/unsupervised anomaly detection.

**Architecture decision (2026-07):** Unsupervised anomaly detection is the primary approach (not supervised classification). The 6 classifier scripts in `codes/python/machine learning/` are early experiments. See `thesis_roadmap.md` (779 lines) for the full 10-phase project plan, architecture rationale, and validation strategy. That file is the authoritative project plan — every task in this repo maps to it.

## Firmware (Arduino / ESP32)

- All sketches target **ESP32** (Arduino framework), opened via **Arduino IDE**.
- **No build system.** Libraries live in `codes/prototyping/libraries/` and `codes/testing/libraries/` — copy or symlink into `Arduino/libraries/`.
- Serial monitor baud: **115200** (set in every sketch).
- BME280 I2C address: **`0x76`** (not the Adafruit default `0x77`).

### Calibration factors (duplicated across all sensor sketches)

| Sensor | Formula |
|--------|---------|
| BME280 temp | `raw * 1.0294412` |
| BME280 humidity | `raw * 1.0579399` |
| Probe A | `1.701471 + 0.984997 * raw` |
| Probe B / C | `1.637417 + 0.9783362 * raw` |

Probe A/B/C DeviceAddress arrays hardcoded in each sketch (OneWire GPIO10).

### MPU6050 calibration offsets (hardcoded in accel_sender)

From `calibration/mpu6050_raw_20260713_152545.csv`:
```
AX_BIAS = -0.005124, AY_BIAS = -0.265409, AZ_BIAS = 0.379842
```

### ESP-NOW — prototyping system (3 boards)

Sketches: `codes/prototyping/{accel_sender, ambient_sender, receiver}/`

- **`prototyping/now_ambient_sender/` and `prototyping/now_receiver_supabase/` are empty dirs.** The actual sketches live in `codes/testing/` only.
- **Shared struct** (`EspNowPacket`): `uint8_t type` (0=accel, 1=ambient) + `float data[6]`
- **MAC addresses:**
  - Accel sender: `E0:72:A1:72:22:94`
  - Ambient sender: `E0:72:A1:72:29:00`
  - Receiver: `E0:72:A1:6F:F8:6C`
- Senders scan for SSID `PLDTHOMEFIBRd2228` for channel; hardcoded channel 11 as fallback.
- **ESP-NOW receive callback must only set a flag** (`volatile bool newDataReady`). Processing runs in `loop()` — never in ISR.
- Send rate: 3 seconds. Receiver prints both data streams to Serial.
- Flash order (1 USB cable): flash senders first (unplug between), receiver last (keep plugged for serial monitoring).
- See `codes/prototyping/PLAN.md` for full architecture. **Note:** PLAN.md lists an older receiver MAC (`0x14:63:93:8C:FC:78`); the code above is the source of truth.

### ESP-NOW — testing sketches

`codes/testing/now_ambient_sender/` → `codes/testing/now_receiver_supabase/`

- Uses older `EspNowData` struct (`temp`, `humid`, `counter`, `a_temp`, `b_temp`, `c_temp`) — no `type` field.
- Receiver MAC (older): `0x14:63:93:8C:FC:78`.
- Supabase table: `readings`, columns: `temperature`, `humidity`, `counter`, `a_temp`, `b_temp`, `c_temp`.
- Receiver WiFi credentials + Supabase URL/key hardcoded.
- See `codes/codes_readme.md` for per-sketch details on all testing sketches.

### TFT display

Sketch: `codes/prototyping/tft_complete/` (ST7789 240×320, SPI)

- Touch: XPT2046 (shared SPI CLK). Full pinout in `designs/tft_display/design_readme.md` — set in TFT_eSPI `User_Setup.h`.
- **No runtime image decoder.** Convert PNG/JPG to RGB565 PROGMEM arrays (`pushImage`).
- Fonts: VLW format, stored as `.h` PROGMEM arrays in `fonts/`, loaded via `loadFont()`.
- Color palette: `#define` macros in the sketch (light/dark Iron Grey modes).

## Python

```
cd "codes/python/machine learning"
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r ../requirements.txt
```

- Requires **Python 3.11+**; deps pinned in `codes/python/requirements.txt` (numpy, matplotlib, scikit-learn, pandas, pyserial, torch). CUDA torch is unused by current scripts.
- `helper.py` provides `plot_decision_regions()` shared by all 6 classifier scripts (0–5).
- `capture_mpu6050.py` — serial capture tool for MPU6050 calibration: collects 200 raw samples, saves to timestamped CSV, prints calibration results.
- `pre-processing/` has 3 scripts (`6 missing values.py`, `7 handling_categorical.py`, `8 feature_extraction`).

## Structure

```
thesis/
├── codes/
│   ├── prototyping/               # Final + ESP-NOW sketches
│   │   ├── accel_sender/          # MPU6050 → ESP-NOW (type=0)
│   │   ├── ambient_sender/        # BME280+DS18B20 → ESP-NOW (type=1)
│   │   ├── receiver/              # Receives both → Serial
│   │   ├── ambient_module_final/  # BME280 + 3×DS18B20 (sensor-only, no wireless)
│   │   ├── mpu6050_calibration/   # MPU6050 bias calibration
│   │   ├── tft_complete/          # ST7789 TFT UI
│   │   ├── libraries/             # Dependencies
│   │   └── PLAN.md                # ESP-NOW architecture plan
│   ├── testing/                   # 23 standalone component sketches
│   │   ├── now_ambient_sender/    # ESP-NOW sender (older, → Supabase)
│   │   ├── now_receiver_supabase/ # ESP-NOW receiver → Supabase
│   │   ├── mpu6050/               # MPU6050 basic test
│   │   └── ...                    # BME280, probes, tft_*, supabase, etc.
│   └── python/
│       ├── machine learning/      # 6 classifiers + pre-processing/
│       │   └── capture_mpu6050.py
│       └── deep learning/         # torch_version.py only (empty placeholder)
├── calibration/                   # MPU6050 raw CSV captures
├── designs/                       # TFT mockups, fonts, palette, logos
├── schematics/                    # Fritzing .fzz files
├── documents/                     # Thesis chapter drafts + suggestion files
├── scripts/                       # Google Docs API scripts (build roadmap/final docs)
├── resources/                     # PDF references (ISLR, ML textbooks, etc.)
├── suggestions/                   # Phase 1 suggestions
└── thesis_roadmap.md              # Authoritative 10-phase project plan
```

## What is NOT here

- CI/CD, linters, formatters, type checkers, test frameworks.
- Root `.gitignore` (only `codes/python/machine learning/.gitignore` exists).
- Package manager config at repo root.
