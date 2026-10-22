# AGENTS.md

Bachelor's thesis — Predictive Maintenance for Coiled Evaporators: ESP32-C3 + BME280/DS18B20/MPU6050 sensors, ESP-NOW, ST7789 TFT, Supabase, and ML.

**Architecture:** unsupervised anomaly detection is the primary approach; supervised classification is secondary/conditional. `thesis_roadmap.md` is the authoritative 10-phase plan. The six `0–5` classifiers in `codes/python/machine learning/` are Iris textbook exercises — no sensor-data or anomaly-detection pipeline is implemented yet.

## Start here

- No CI, tests, linter, formatter, or root package manager. Firmware verification is manual: compile/flash in Arduino IDE and watch Serial at 115200.
- Docs drift from code: `README.md` and `codes/codes_readme.md` put `now_ambient_sender` and `now_receiver_supabase` under `prototyping/` (they only exist under `testing/`) and imply an integrated receiver → TFT → Supabase pipeline. `codes/prototyping/PLAN.md` has an old receiver MAC. Trust the `.ino` files.
- Active firmware is three separate pieces: two senders + a serial-only receiver. `tft_complete` is a standalone TFT UI; ESP-NOW → Supabase upload exists only in the older `testing/now_receiver_supabase`.

## Firmware (Arduino / ESP32)

- Target **ESP32-C3 Super Mini**, opened in **Arduino IDE**. No PlatformIO/CLI build.
- Requires ESP32 Arduino core **3.x**: the active senders/receiver use the newer `wifi_tx_info_t` / `esp_now_recv_info_t` callback signatures, so older cores won't compile them.
- Libraries are vendored in `codes/prototyping/libraries/` and `codes/testing/libraries/` (near-duplicate snapshots); treat them as dependencies, not project code. Arduino resolves includes from the sketchbook, so copy or symlink the needed library into `Arduino/libraries/`.
- Serial monitor **115200** for the active sketches; exceptions: `testing/BME280` (9600) and `testing/tft_custom_fonts` (250000). BME280 I2C address **`0x76`** (not Adafruit's default `0x77`). DS18B20 OneWire is **`ONE_WIRE_BUS 10`**; comments in `ambient_module_final` and `probes` say GPIO15, but the define is authoritative. Probe addresses are hardcoded in each sketch.

### Hardcoded calibration

| Sensor | Formula |
|--------|---------|
| BME280 temp | `raw * 1.0294412` |
| BME280 humidity | `raw * 1.0579399` |
| Probe A | `1.701471 + 0.984997 * raw` |
| Probe B / C | `1.637417 + 0.9783362 * raw` |

MPU6050 biases from `calibration/mpu6050_raw_20260713_152545.csv`:
`AX_BIAS = -0.005124`, `AY_BIAS = -0.265409`, `AZ_BIAS = 0.379842`.

### ESP-NOW — active prototype (3 boards)

- `codes/prototyping/{accel_sender, ambient_sender, receiver}/`; `ambient_module_final/` is the same sensors without wireless.
- Shared struct (`EspNowPacket`): `uint8_t type` + `float data[6]`.
  - `type=0` (accel): `data[0..2] = ax, ay, az`; rest zero.
  - `type=1` (ambient): `data[0..5] = temp, humidity, counter, probeA, probeB, probeC`.
- MACs: accel `E0:72:A1:72:22:94`, ambient `E0:72:A1:72:29:00`, receiver `E0:72:A1:6F:F8:6C`.
- Senders scan for SSID `PLDTHOMEFIBRd2228` and set the WiFi channel, but `peerInfo.channel` is hardcoded to 11 — keep the `esp_wifi_set_channel()` value and `peerInfo.channel` aligned. Send every 3 s.
- **Receive callback must stay minimal: copy the packet and set `volatile bool newDataReady`; parse/upload in `loop()`, never in the callback.**
- If packets don't arrive, check channel alignment: the receiver never calls `esp_wifi_set_channel` (`peerInfo.channel = 0`), so it listens on whatever channel it booted with.
- Flash order with one USB cable: accel sender, then ambient sender (unplug between), receiver last (leave connected for Serial).

### ESP-NOW — older testing generation

- `codes/testing/now_ambient_sender/` → `now_receiver_supabase/` uses the older `EspNowData` (no `type` field), receiver MAC `14:63:93:8C:FC:78`, and Supabase table `readings` (`temperature`, `humidity`, `counter`, `a_temp`, `b_temp`, `c_temp`).
- Do not mix the two packet structs or MAC sets. The testing receiver has hardcoded WiFi/Supabase credentials — don't copy them into new files or paste them into logs.

### TFT

- `codes/prototyping/tft_complete/` is a multi-file sketch: `.ino` + `helper_functions.*` + `assets/` (RGB565) + `fonts/` (VLW).
- Documented panel is **ST7789 240×320**; touch is **XPT2046**. Pinout: TFT CS 7, RST 3, DC 2, MOSI 6, SCK 4, MISO 5; touch CS 8 (full table in `designs/tft_display/design_readme.md`).
- The vendored `libraries/TFT_eSPI/User_Setup.h` is still the stock ILI9341/ESP8266 default — don't use it to infer project driver/pins. If the display is wrong, check the `User_Setup.h` in the library copy Arduino actually compiles.
- No runtime image decoder: convert images to RGB565 PROGMEM arrays (`pushImage`). Fonts are VLW `.h` PROGMEM arrays loaded with `loadFont()`.

## Python

```
cd "codes/python/machine learning"
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r ../requirements.txt
```

- Python **3.11+**. `codes/python/requirements.txt` pins numpy/matplotlib/scikit-learn/pandas/pyserial/torch. torch is only used by `deep learning/torch_version.py` (a CUDA check); the classifiers don't need it, so a lighter `pip install numpy matplotlib scikit-learn pandas` is enough for them.
- Scripts `0–5` are sklearn **Iris** exercises; `pre-processing/6–8` use synthetic/wine data. None read ESP32/sensor data. All classifier scripts call `plt.show()`, so don't run them as a headless verification step.
- `helper.py` provides the shared `plot_decision_regions()`.
- `capture_mpu6050.py`: run alongside the `prototyping/mpu6050_calibration` sketch; it waits for the `ax_raw,...` header, captures 200 samples, and writes `mpu6050_raw_<timestamp>.csv` **to the current directory** — run it from `calibration/` if that's where you want the file.
- `pre-processing/8 feature_extraction` has no `.py` extension and imports `tabulate`, which is not pinned in `requirements.txt`.

## Google Docs scripts

`scripts/*.py` are one-off Google Docs publishers, not part of the firmware/ML workflow. They hardcode the old path `D:/School/1 Projects/thesis/...` and load an OAuth token from `~/AppData/Local/hermes/google_token.json`; their Google API dependencies are not in `requirements.txt`. Don't run or fix them unless the task is about the docs pipeline.

## Layout

- `codes/prototyping/` — active 3-board firmware + `tft_complete/`.
- `codes/testing/` — per-component sketches (BME280, probes, MPU6050, TFT, ESP-NOW, Supabase).
- `codes/python/` — ML exercises; `deep learning/torch_version.py` is a CUDA check only.
- `calibration/` — MPU6050 raw capture.
- `designs/tft_display/` — TFT mockups/pinout; `schematics/` — Fritzing/KiCad.
- `documents/draft/` — working chapter drafts; `documents/original/` — baseline copies; `documents/suggestions/` — review notes.
- `thesis_roadmap.md` — authoritative plan.
