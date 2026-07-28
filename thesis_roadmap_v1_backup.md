# Thesis Roadmap — Predictive Maintenance for Coiled Evaporators

> Last updated: YYYY-MM-DD  
> Status: ███████░░░ XX% complete  
> Group: John Ronald Pacaldo · Collin Brandon Asio · Simon France Sulibio

---

## Legend

| Emoji | Type |
|--------|------|
| 📝 | Paper Overhaul |
| 🔧 | Prototyping |
| 💻 | Coding |
| 🤖 | Machine Learning |
| 📊 | Data Collection |
| 🚀 | Deployment |
| 📋 | Documentation |

| Priority | Symbol |
|----------|--------|
| Critical | 🔴 |
| High | 🟠 |
| Medium | 🟡 |
| Low | 🟢 |

| Status | Symbol |
|--------|--------|
| Not started | ⬜ |
| In progress | 🔄 |
| Blocked | 🚫 |
| Completed | ✅ |

---

## Phase 1 — Paper Overhaul: Foundation

### Chapter 1 — Introduction

- [ ] 🔴 **Fix variable-sensor mapping** — `1.4 Conceptual Framework`
  - Reconcile independent variables (air temperature, noise, ice build-up, refrigerant leaks) with actual hardware
  - Either add acoustic sensor + refrigerant leak sensor to hardware plan, or remove noise/leak from framework
  - Create explicit mapping table: Variable → Sensor → Data Type → Model Input

- [ ] 🔴 **Define expert-validated labeling criteria** — `1.1 / 3.1.5`
  - Define quantitative thresholds: "Abnormal = visible frost > 20% coil surface OR inlet-outlet ΔT < 3°C OR compressor current > X A"
  - Name the experts consulted and their qualifications
  - Include criteria in the methodology section

- [ ] 🟠 **Strengthen RA 11285 rationale** — `1.1`
  - Add paragraph quantifying potential energy savings from PdM at Xavier University
  - Cite reported 6.4% energy increase from 30% fouling (Niknami et al., 2024)
  - Estimate: "N AC units × avg consumption × 6.4% × ₱/kWh = ₱X annual savings"

- [ ] 🟠 **Add testable hypotheses** — `1.2`
  - H1: At least one ML model achieves F1 ≥ 0.85 for binary normal/abnormal classification
  - H2: PCA-reduced features achieve comparable performance to full 11-feature dataset
  - H3: Hybrid CNN+RF outperforms standalone RF by ≥ 2% F1

- [ ] 🟡 **Reframe RQ3 for testability** — `1.1`
  - Current: "How can the framework integrate real-time data collection…"
  - Suggested: "What is the end-to-end latency from sensor reading to dashboard update in self-hosted vs. cloud-based deployment?"

- [ ] 🟡 **Justify binary classification choice** — `1.5`
  - Add argument: binary classification is industry standard for initial PdM; more actionable than continuous score
  - If regression is revisited later, it becomes a future work item

- [ ] 🟢 **Add scope diagram** — `1.5`
  - Visual: what's in scope (50 units, 3 locations, 6 models, binary classification) vs. out of scope (regression, multi-fault identification, mobile app)

### Chapter 3 — Methodology (Pre-Prototyping Sections)

- [ ] 🔴 **Clarify monitoring regime** — `3.1.1`
  - State explicitly: continuous installation (sensors permanently mounted) OR weekly visit protocol (portable kit, 10 trials, removed)
  - This fundamentally affects data characteristics and affects the entire downstream pipeline
  - If weekly visits: rename "6-month monitoring" to "6-month study with weekly measurements" throughout

- [ ] 🔴 **Resolve ESP32-CAM image transmission path** — `3.1.4`
  - ESP-NOW payload = 250 bytes; a single QVGA JPEG = 10–50 KB → cannot transmit images via ESP-NOW
  - Choose and document one approach:
    - Option A: On-device TinyML (quantized CNN on ESP32-CAM, send classification label only)
    - Option B: Wi-Fi HTTP/MQTT image upload to Ingest Server
    - Option C: SD card storage, manual transfer weekly
  - Recommend Option A — aligns with edge computing literature

- [ ] 🔴 **Add sampling parameters table** — `3.1.5`
  - Per sensor: sampling rate (Hz), trial duration (min), readings per trial
  - Total expected data volume per unit per visit
  - Example: BME280 @ 1 Hz × 5 min trial = 300 readings/trial

- [ ] 🟠 **Add system architecture diagram** — `3.1.4`
  - All 3 node types with sensors, power sources, communication paths
  - Data flow: Node → Master (ESP-NOW) → Ingest Server (Wi-Fi) → NAS → Cloud
  - Clearly distinguish ESP-NOW path (sensor readings) from Wi-Fi path (images/config)

- [ ] 🟠 **Address ESP32-C3 ADC limitations** — `3.1.4`
  - Document ESP32-C3 ADC noise (ENOB ~9–10 bits) for ACS712 analog readings
  - Consider external 16-bit ADC (ADS1115) or digital current sensor (INA219) for fan motor current
  - If using onboard ADC: specify averaging strategy (>1000 samples) and expected accuracy

- [ ] 🟡 **Add power management plan** — `3.1.4`
  - Power source per node (USB, battery, AC unit tap)
  - Battery life estimate if portable
  - Sleep/wake cycles for energy optimization

- [ ] 🟡 **Define sensor failure protocol** — `3.1.5`
  - DS18B20 disconnect → flag row, continue remaining sensors
  - ESP32-CAM blurry image → re-capture, max 3 attempts
  - Malformed readings → log, skip, alert

- [ ] 🔴 **Nested: 🔧 Hardware BOM finalization** — `3.1.4`
  - Finalize Bill of Materials: 50× BME280, 150× DS18B20, 100× ACS712, 50× ZMPT101B, 50× ESP32-C3, 50× ESP32-CAM
  - Per-unit cost estimate
  - Sourcing plan (orders, lead times)

---

## Phase 2 — Prototyping: Hardware Validation

### Sensor Nodes

- [ ] 🔴 **🔧 Assemble Thermal Node prototype** — `ambient_module_final/`
  - ESP32-C3 + BME280 (I2C 0x76) + 3× DS18B20 (OneWire GPIO10)
  - Verify all 4 sensors read simultaneously
  - Apply calibration factors as hardcoded constants
  - Serial monitor output format: `Temp=XX.X Hum=XX.X Counter=X A=XX.X B=XX.X C=XX.X`

- [ ] 🔴 **🔧 Assemble Electrical Node prototype**
  - ESP32-C3 + 2× ACS712 + ZMPT101B
  - Verify current and voltage readings with reference DMM
  - Measure and record zero-current offset for both ACS712 channels
  - Test with known resistive loads (50W, 200W bulbs)

- [ ] 🔴 **🔧 Assemble Frost Node prototype**
  - ESP32-CAM image capture at regular interval
  - Test image quality under various lighting conditions (HVAC unit interior)
  - Baseline image size (JPEG quality vs. file size)
  - If on-device CNN: test Edge Impulse model export → Arduino

### ESP-NOW Communication

- [ ] 🔴 **🔧 ESP-NOW master-slave pairing**
  - 3 senders (Thermal, Electrical, Frost) → 1 Master ESP32
  - Test channel scanning via SSID `PLDTHOMEFIBRd2228`; fallback channel 11
  - Verify MAC addresses: Accel `E0:72:A1:72:22:94`, Ambient `E0:72:A1:72:29:00`, Receiver `E0:72:A1:6F:F8:6C`
  - Test 3-second send interval stability over 1-hour continuous run

- [ ] 🟠 **🔧 Timestamp synchronization protocol**
  - Master broadcasts sync pulse → all nodes timestamp readings
  - Verify all 3 nodes report same timestamp within ±50ms tolerance
  - Test over 30-minute run

- [ ] 🟡 **🔧 Data struct validation**
  - Verify `EspNowPacket` struct (type + 6 floats) matches across all nodes
  - Test edge cases: NaN values, sensor disconnect (default to 0.0 or -999.0)

### TFT Display UI

- [ ] 🟡 **🔧 TFT complete UI** — `tft_complete/`
  - ST7789 240×320 SPI + XPT2046 touch
  - Pages: Main Menu → Pairing → Devices → Units → System
  - Display live sensor data from Master ESP32 via Serial/UART
  - Color palette: Iron Grey light/dark modes (macros in sketch)

### Firmware Coding

- [ ] 🔴 **💻 Calibration factor integration**
  - Embed verified calibration constants in all sensor sketches
  - BME280: `T_cal = T_raw × 1.0294412`, `H_cal = H_raw × 1.0579399`
  - DS18B20 A: `1.701471 + 0.984997 × raw`
  - DS18B20 B/C: `1.637417 + 0.9783362 × raw`
  - ACS712: `ADC − ADC_Zero_Offset` → calibrated current via sensitivity factor

- [ ] 🟠 **💻 Data formatting script**
  - Master ESP32 outputs structured CSV line: `timestamp,unit_id,temp,humid,pressure,inlet,outlet,coil,comp_current,fan_current,voltage,frost,coil_cond`
  - Ingest Server ingestion script: reads serial, validates format, writes to `02_Data/raw/`

- [ ] 🟡 **💻 Supabase integration** (optional — testing sketch)
  - Test ESP32 → Supabase insert for `readings` table
  - Verify JSON format: `{"temperature":X, "humidity":X, "counter":X, "a_temp":X, "b_temp":X, "c_temp":X}`

### Nested Paper Tasks

- [ ] 🟡 **📝 Update Chapter 3** from prototyping learnings
  - Record actual vs. expected sensor accuracy
  - Document any hardware substitutions
  - Update system architecture diagram with final wiring

---

## Phase 3 — Paper Overhaul: Literature & Gaps

### Chapter 2 — Review of Related Literature

- [ ] 🔴 **📝 Add synthesis matrix** — `2.11 (new section)`
  - Multi-dimensional comparison table: Study | Model | Dataset size | Accuracy | Sensor types | HVAC type | Deployment context | Limitation
  - Write 3–5 explicit research gaps this thesis addresses

- [ ] 🔴 **📝 Replace tangential studies**
  - Remove 2.8 (Aji et al., magnetic sensors — not HVAC)
  - Remove 2.9 (Abood et al., electromechanical motors — not HVAC)
  - Replace with:
    - Study on low-cost sensor calibration for predictive maintenance
    - Study on evaporator coil fouling detection (expand Niknami et al., 2024)
    - Study on ESP32/edge computing for building monitoring

- [ ] 🟠 **📝 Reconcile calibration formula with literature**
  - Fix Probe B regression output: either update R output screenshot or correct formula
  - Ensure all calibration formulas in Chapter 4 match firmware codebase exactly

- [ ] 🟡 **📝 Cite foundational ML papers**
  - Add: Breiman (2001) for Random Forest, Chen & Guestrin (2016) for XGBoost, Cortes & Vapnik (1995) for SVM
  - Don't rely solely on Sarker (2021) for all algorithm descriptions

- [ ] 🟡 **📝 Add conceptual framework diagram from literature**
  - Visual showing: literature findings → informs this thesis's architecture
  - Highlight unique contribution: ESP32 + ESP-NOW + low-cost sensors + hybrid CNN+RF

### Nested ML Tasks

- [ ] 🟠 **🤖 Final model selection**
  - Confirm: RF, XGBoost, k-NN, RBF SVM, DNN, Hybrid CNN+RF
  - Add justification paragraph for each (why included, why not others)
  - Consider adding Logistic Regression as baseline (simplest interpretable model)

---

## Phase 4 — Sensor Calibration: Remaining Sensors

### ACS712 Current Calibration

- [ ] 🔴 **📊 Zero-offset calibration** — both ACS712 channels
  - Node powered on, no load connected
  - 1000 ADC readings over 60 seconds per sensor
  - Compute: `ADC_Zero_Offset = mean(1000 readings)`
  - Store per-sensor UID in calibration database (`01_Sensor_Calibration/`)

- [ ] 🔴 **📊 Sensitivity (gain) calibration**
  - Connect known resistive loads: 50W, 200W, 250W bulbs
  - Measure True-RMS current with reference DMM (Fluke 115 or equivalent)
  - Linear regression per sensor: `I_actual = m × (ADC_raw − ADC_Zero_Offset) + c`
  - If non-linear at low currents → use piecewise or polynomial fit

### ZMPT101B Voltage Calibration

- [ ] 🔴 **📊 Trimpot standardization**
  - Adjust onboard potentiometer: 250V input → ADC output ~640 (below saturation)
  - Standardize across all 50 modules

- [ ] 🔴 **📊 3rd-order polynomial calibration**
  - Variac: 10 voltage setpoints from 50V to 250V
  - Record ADC reading vs. True-RMS DMM reference
  - Fit 3rd-order polynomial per sensor: `V_actual = a₀ + a₁·ADC + a₂·ADC² + a₃·ADC³`
  - Report R² and max absolute error

### Calibration Database

- [ ] 🟠 **💻 Calibration database script**
  - JSON or CSV per sensor type: `{UID: {type: "linear"|"polynomial", coefficients: [...]}}`
  - Version control the calibration database in `01_Sensor_Calibration/`
  - Python helper: `apply_ccf(uid, raw_value) → calibrated_value`

- [ ] 🟡 **💻 Automated CCF application**
  - Preprocessing pipeline reads raw CSV → looks up UID → applies CCF → writes to `02_Data/interim/`
  - Includes unit test: known raw value → verify calibrated output matches expected

### Nested Paper Tasks

- [ ] 🟠 **📝 Write Chapter 4 sensors calibration results**
  - Include figure: scatter plot per sensor (sensor vs. reference with regression line)
  - Include figure: residual plot per sensor
  - Report R², RMSE, max error on held-out validation set (80/20 split)
  - Fix Probe A data error (`17.3` → `27.3`) before analysis
  - Reconcile Probe B formula (regression output vs. stated formula)

---

## Phase 5 — Paper Overhaul: Methodology Details

- [ ] 🔴 **📝 Condense Chapter 3.3 Model Development section**
  - Cut ~40 pages of textbook content (linear regression, gradient descent, backpropagation derivations)
  - Move mathematical derivations to an Appendix
  - Keep in main text: 1–2 paragraph summary per model + architecture specification table

- [ ] 🔴 **📝 Define DNN architecture**
  - Input layer: 11 features (or k PCA components)
  - Hidden layers: e.g., Dense(64, ReLU) → Dropout(0.3) → Dense(32, ReLU) → Dropout(0.3)
  - Output layer: Dense(1, Sigmoid) for binary classification
  - Loss: Binary Cross-Entropy
  - Optimizer: Adam, learning rate 0.001
  - Batch size: 32, epochs: 100 (early stopping patience 10)

- [ ] 🔴 **📝 Define CNN architecture**
  - Input: e.g., 224×224×3 (or native ESP32-CAM resolution)
  - Architecture: Transfer learning (MobileNetV2 or custom)
    - Conv2D(32, 3×3) → MaxPool(2×2) → Conv2D(64, 3×3) → MaxPool(2×2) → Conv2D(128, 3×3) → MaxPool(2×2) → Flatten → Dense(128) → Dropout(0.5) → Dense(2, Softmax)
  - Loss: Categorical Cross-Entropy
  - Data augmentation: random horizontal flip, ±10% brightness, ±10° rotation
  - Batch size: 16, epochs: 50 (early stopping patience 10)

- [ ] 🔴 **📝 Define Hybrid CNN+RF architecture**
  - Two-stage pipeline:
    - Stage 1: ESP32-CAM image → CNN → frost probability [0,1] + coil condition probability [0,1]
    - Stage 2: 9 sensor features + 2 CNN probabilities → Random Forest → normal/abnormal
  - Alternative: CNN penultimate layer (128-dim feature vector) + 9 sensor features → RF
  - Include architecture diagram

- [ ] 🟠 **📝 Specify hyperparameter search space** per model
  - RF: n_estimators [50, 100, 200, 500], max_depth [5, 10, 20, None], min_samples_leaf [1, 2, 5]
  - XGBoost: n_estimators [100, 300, 500], max_depth [3, 6, 9], learning_rate [0.01, 0.1, 0.3]
  - k-NN: k [3, 5, 7, 9, 11], metric [euclidean, manhattan], weights [uniform, distance]
  - SVM: C [0.1, 1, 10, 100], gamma [scale, auto, 0.01, 0.1]
  - DNN: layers [1, 2, 3], neurons [32, 64, 128], dropout [0.2, 0.3, 0.5], lr [0.001, 0.0001]

- [ ] 🟡 **📝 Add overfitting mitigation section**
  - DNN/CNN: Dropout, L2 regularization, early stopping, batch normalization
  - RF: max_depth, min_samples_leaf, n_estimators
  - SVM: C (regularization), gamma (kernel width)
  - k-NN: k selection, distance weighting

### Nested Coding Tasks

- [ ] 🟡 **💻 Python environment setup**
  - Activate venv: `cd "codes/python/machine learning"; python -m venv .venv; .venv\Scripts\Activate.ps1`
  - Install deps: `pip install -r ../requirements.txt`
  - Verify: `python -c "import numpy, matplotlib, sklearn, pandas, torch; print('OK')"`

- [ ] 🟡 **💻 Project scaffolding**
  - Create `03_Code/` directory structure (ingest, preprocessing, modeling subdirs)
  - Initialize Git for code tracking
  - Create `config.yaml` for paths, parameters, model configs

---

## Phase 6 — Data Collection

### Hardware Deployment

- [ ] 🔴 **📊 Deploy sensor nodes to 50 AC units**
  - SBM-AVR: ~15 units
  - College of Engineering: ~25 units
  - Faber Hall 1st floor: ~10 units
  - Install, test connectivity, assign UnitID

- [ ] 🔴 **📊 Weekly data collection sessions** — 6 months
  - Each visit: 10 trials per unit per week
  - Each trial: X minutes of continuous readings at specified sampling rate
  - Record: ambient temp, humidity, pressure, inlet/outlet/coil temp, compressor/fan current, voltage
  - Also: One ESP32-CAM still image per trial (or N images)

- [ ] 🔴 **📊 Image labeling** — frost / coil condition
  - Label each image: Normal / Frost present / Fouled coils / Both
  - Expert validation: have HVAC technician/PE verify a random 10% sample
  - Compute inter-rater agreement (Cohen's Kappa) if multiple labelers

### Data Pipeline

- [ ] 🔴 **💻 Data ingestion script**
  - Reads serial/MQTT from Master ESP32
  - Validates format (expected columns, ranges)
  - Writes to `02_Data/raw/` with naming convention: `YYYYMMDDTHHmmSSZ_<Location>_<UnitID>_<TrialNum>_RAW.csv`

- [ ] 🟠 **💻 Data cleaning & CCF application**
  - Script reads `02_Data/raw/` → applies CCFs from `01_Sensor_Calibration/` → validates ranges → writes to `02_Data/interim/`
  - Handles missing values: forward-fill short gaps (<5 readings), flag longer gaps
  - Detects and flags outliers (outside 3σ or manual thresholds)

- [ ] 🟠 **💻 Feature engineering** for interim → processed
  - Rolling window statistics per trial: mean, std, min, max, slope
  - Rate-of-change features: Δ(Inlet−Outlet)/Δt, ΔCoilTemp/Δt
  - Derived COP proxy: (Inlet − Outlet) / Compressor Current

- [ ] 🟡 **💻 Data validation dashboard** (optional)
  - Simple Streamlit page: per-unit data completeness, sensor health, weekly trial count
  - Alerts if unit has <10 trials in a week

### Nested Paper Tasks

- [ ] 🟡 **📝 Update Chapter 3 DMP section**
  - Replace theoretical DMP with actual implementation notes
  - Record any deviations from planned storage/backup strategy
  - Document actual file counts, data volumes

---

## Phase 7 — Machine Learning: CNN (Image Classification)

- [ ] 🔴 **🤖 Prepare image dataset**
  - Organize labeled images: train/val/test splits per class
  - Class balance check — if imbalanced, apply augmentation or weighted loss

- [ ] 🔴 **🤖 Train CNN model**
  - Implement in PyTorch or TensorFlow/Keras
  - Track training/validation loss and accuracy per epoch
  - Save best model (lowest val_loss) as `cnn_frost_classifier.pth`

- [ ] 🟠 **🤖 CNN evaluation**
  - Confusion matrix: Frost / No Frost / Fouled / Clean
  - Per-class precision, recall, F1
  - Overall accuracy
  - Confusion matrix plot

- [ ] 🟡 **🤖 Ablation study** (if time permits)
  - Compare: Transfer learning (MobileNetV2) vs. custom CNN from scratch
  - Compare: With/without data augmentation
  - Report results

- [ ] 🟡 **💻 Edge deployment (optional)**
  - If on-device: quantize model (INT8) via Edge Impulse or TensorFlow Lite
  - Export to Arduino-compatible C array
  - Benchmark inference time on ESP32-CAM

### Nested Paper Tasks

- [ ] 🟠 **📝 Write Chapter 4 CNN results**
  - Report: architecture choice, dataset size, class distribution, training curves, evaluation metrics
  - Include: confusion matrix figure, sample predictions (image + predicted label + confidence)

---

## Phase 8 — Machine Learning: Sensor Classifiers

### Preprocessing Pipeline

- [ ] 🔴 **🤖 Complete preprocessing pipeline**
  - Implementation in `03_Code/2_preprocessing/`
  - Standardization: fit on train only, transform val/test
  - One-hot encoding: frost label, coil condition label → binary columns
  - PCA: fit on train, transform val/test; plot variance explained; select k with ≥95% cumulative
  - Output: X_train, X_val, X_test, y_train, y_val, y_test saved to `02_Data/processed/`

- [ ] 🟠 **🤖 Class imbalance handling**
  - Check class distribution (Normal vs. Abnormal)
  - If ratio > 3:1, apply SMOTE on training set only
  - Report pre- and post-balancing class counts

### Model Training

- [ ] 🔴 **🤖 Train RF classifier**
  - Hyperparameter tuning via GridSearchCV (5-fold inner CV)
  - Best params → final training → save `rf_classifier.pkl`
  - Feature importance plot (top features for normal vs. abnormal)

- [ ] 🔴 **🤖 Train XGBoost classifier**
  - GridSearchCV tuning
  - Feature importance (gain, weight, cover)

- [ ] 🔴 **🤖 Train k-NN classifier**
  - k selection via elbow method (accuracy vs. k curve)
  - Test Euclidean vs. Manhattan distance

- [ ] 🔴 **🤖 Train RBF SVM classifier**
  - GridSearchCV: C, gamma
  - Note: may need subsampling if dataset > 10K rows (SVM scales quadratically)

- [ ] 🔴 **🤖 Train DNN classifier**
  - PyTorch implementation
  - Training loop with early stopping
  - Save `dnn_classifier.pth`

- [ ] 🔴 **🤖 Train Hybrid CNN+RF**
  - Feed image(s) through trained CNN → extract probabilities or penultimate features
  - Concatenate with sensor features
  - Train RF on combined feature set
  - Save `hybrid_cnn_rf.pkl`

### Model Evaluation

- [ ] 🔴 **🤖 Evaluate all models on held-out test set**
  - Per model: confusion matrix, accuracy, precision (Normal), recall (Normal), precision (Abnormal), recall (Abnormal), F1 (macro), F1 (weighted)
  - Single comparison table with all 6 models and all metrics

- [ ] 🔴 **🤖 Friedman test + Nemenyi post-hoc**
  - 30 subsets → accuracy per model per subset
  - Friedman test: H₀ rejected if p < 0.05
  - Nemenyi post-hoc: pairwise critical difference
  - CD (Critical Difference) diagram: rank models, connect non-significantly-different groups

- [ ] 🟠 **🤖 Error analysis**
  - For best model: examine misclassified samples
  - What features distinguish correctly vs. incorrectly classified samples?
  - Any systematic pattern? (e.g., all misclassifications from a specific building or unit type)

- [ ] 🟡 **🤖 Ablation study** (optional)
  - Compare: Full 11 features vs. PCA-reduced vs. sensor-only (no CNN image features)
  - Quantify contribution of image-based features to model performance

### Nested Paper Tasks

- [ ] 🟠 **📝 Write Chapter 4 ML results**
  - Results table: all 6 models × all metrics
  - CD diagram from Nemenyi test
  - Feature importance plot (RF)
  - One confusion matrix for best model
  - Interpretation: which model is best and why?

---

## Phase 9 — Deployment

### Server Setup

- [ ] 🔴 **🚀 Ingest Server configuration**
  - Set up dedicated PC or Raspberry Pi with Python environment
  - Configure Wi-Fi network (same as Master ESP32)
  - Install: Python 3.11+, watchdog, streamlit, joblib, pandas, numpy, scikit-learn, sqlite3
  - Set up NAS mount point + directory structure from DMP

- [ ] 🔴 **💻 Ingest service script**
  - Reads serial/Socket from Master ESP32
  - Validates and writes to `02_Data/raw/`
  - Runs as persistent background service (systemd or Windows Service)

### Inference Pipeline

- [ ] 🔴 **🚀 Watchdog automation setup**
  - Monitor `02_Data/raw/` for new files (use FILE_CLOSED or staging directory + atomic move)
  - Trigger on new complete CSV → load → apply CCFs → preprocess → load model → predict → store result

- [ ] 🔴 **💻 Automated inference script**
  - Load best model (`rf_classifier.pkl` or `hybrid_cnn_rf.pkl`)
  - Load scaler + PCA transformer
  - Predict: 11 features → calibrated → standardized → PCA → model.predict()
  - Store: `{unit_id, timestamp, prediction, confidence, features_snapshot}` → `predictions.db`
  - Error handling: catch NaN, malformed input, shape mismatch → log error → skip file

- [ ] 🟠 **🚀 SQLite predictions database**
  - Schema: `predictions` table with columns: id, unit_id, timestamp, prediction (0/1), confidence (float), features_json (TEXT)
  - Schema: `alerts` table with columns: id, unit_id, timestamp, severity (warning/alert/critical), acknowledged (bool)
  - Create indexes on unit_id, timestamp for query performance

- [ ] 🟡 **💻 Alert threshold logic**
  - Single abnormal → warning
  - 3 consecutive abnormals for same unit → alert
  - 5 consecutive abnormals → critical (email/SMS notification optional)
  - Configurable via `config.yaml`

### Dashboard

- [ ] 🟠 **🚀 Streamlit dashboard — main status page**
  - `app.py` with overview: all 50 units, most recent prediction each, color-coded grid (🟢 Normal / 🔴 Abnormal / ⚪ No data)
  - Auto-refresh every 30 seconds (or triggered by watchdog file event)

- [ ] 🟠 **🚀 Streamlit dashboard — unit detail page**
  - Dropdown: select unit by ID
  - Historical chart: sensor time-series (temp, current, voltage) + prediction overlay
  - Prediction history table: date → prediction → confidence

- [ ] 🟡 **🚀 Streamlit dashboard — admin page**
  - Model retraining trigger button
  - Data collection status (units that haven't reported this week)
  - Alert acknowledgment UI

- [ ] 🟡 **💻 Streamlit authentication** (optional)
  - Simple password protection via environment variable or config
  - Read-only view for maintenance staff, admin view for researchers

### Cloud Sync (Optional)

- [ ] 🟢 **🚀 Supabase cloud backup**
  - Nightly sync script: `predictions.db` → Supabase `readings` table
  - Ensure API key is NOT stored in plaintext (use environment variable)
  - Test connectivity and data integrity

### Nested Paper Tasks

- [ ] 🟠 **📝 Finalize Chapter 3 deployment section**
  - Replace theoretical deployment plan with implementation summary
  - Include: architecture diagram, technology choices, deployment workflow
  - Add dashboard screenshots in Appendix

---

## Phase 10 — Finalization

### Chapter 4 — Complete Results & Discussion

- [ ] 🔴 **📝 Integrate all Chapter 4 subsections**
  - 4.1 Sensor calibration (BME280, DS18B20, ACS712, ZMPT101B)
  - 4.2 CNN image classification results
  - 4.3 Dataset overview (class distribution, PCA results, feature statistics)
  - 4.4 ML model comparison (all 6 models, all metrics)
  - 4.5 Statistical analysis (Friedman + Nemenyi)
  - 4.6 Deployment results (dashboard screenshots, latency, uptime)

- [ ] 🔴 **📝 Discussion per section**
  - Why did model X outperform model Y? Link back to literature
  - Were the hypotheses supported? (H1: F1 ≥ 0.85, H2: PCA comparable, H3: Hybrid > RF)
  - Limitations encountered (sensor noise, dataset size, labeling subjectivity)
  - Implications for Xavier University maintenance practices

### Chapter 5 — Conclusion & Recommendations

- [ ] 🟠 **📝 Write conclusions**
  - Summary of what was built and tested
  - Answer each research question directly
  - Key finding: which model is recommended for deployment and why

- [ ] 🟠 **📝 Write recommendations**
  - For Xavier University PPO: adopt PdM for high-priority AC units, integrate into maintenance workflow
  - For future research: regression models, multi-fault classification, mobile app, longer monitoring, more sensors (acoustic, refrigerant leak)
  - For hardware: upgrade to external ADC, better power management, permanent installation

### Final Deliverables

- [ ] 🟠 **📝 Abstract** — 250–300 words
- [ ] 🟡 **📝 Acknowledgements**
- [ ] 🟡 **📝 Appendices** — calibration data tables, R regression outputs, full code listings, dashboard screenshots
- [ ] 🟡 **📋 APA/citation audit** — check all in-text citations → reference list, consistent format
- [ ] 🟡 **📋 Table of Contents, List of Figures, List of Tables** — auto-generated
- [ ] 🟡 **📋 Defense presentation** — 15–20 slides
  - Problem & motivation
  - Hardware architecture
  - Methodology overview
  - Key results (1 slide per major finding)
  - Conclusions & recommendations
  - Demo video of dashboard (1–2 min)

---

## Milestones & Deadlines

| Date | Milestone | Deliverables |
|------|-----------|-------------|
| YYYY-MM-DD | Phase 1 complete | Ch1 overhaul + Ch3 pre-proto sections |
| YYYY-MM-DD | Phase 2 complete | All 3 nodes assembled, ESP-NOW working, TFT UI functional |
| YYYY-MM-DD | Phase 3 complete | Ch2 overhaul, literature synthesis matrix |
| YYYY-MM-DD | Phase 4 complete | ACS712 + ZMPT101B calibration, calibration database built |
| YYYY-MM-DD | Phase 5 complete | Ch3 model dev section condensed, architectures defined |
| YYYY-MM-DD | Phase 6 complete | 6-month data collection, all 50 units, image labeling |
| YYYY-MM-DD | Phase 7 complete | CNN trained, evaluated, Ch4 CNN results written |
| YYYY-MM-DD | Phase 8 complete | All 6 ML models trained + evaluated, Friedman test, Ch4 ML results written |
| YYYY-MM-DD | Phase 9 complete | Dashboard live, inference pipeline running, Ch3 deployment finalized |
| YYYY-MM-DD | Phase 10 complete | Full thesis draft submitted for adviser review |
| YYYY-MM-DD | Defense | Presentation, demo, Q&A |
| YYYY-MM-DD | Final submission | Hardbound copies + digital archive |

---

## Risk Registry

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Sensor availability (350 units) delayed by supplier | Medium | High | Order early; identify backup suppliers; reduce unit count if needed |
| Calibration equipment not available at XU labs | Medium | High | Verify availability before Phase 1 end; source from partner labs; budget for rental |
| ESP32-CAM image quality poor inside AC unit | Medium | Medium | Test under real conditions early (Phase 2); add LED ring light if needed |
| Class imbalance (too few Abnormal samples) | High | Medium | Apply SMOTE; use class-weighted loss; consider semi-supervised if extreme |
| 6-month timeline insufficient for data collection | Medium | High | Prioritize units with known issues; possibly extend monitoring; reduce trial count |
| Scope too large for 3 members | High | High | Cut non-critical tasks (Supabase cloud sync, edge TinyML deployment) if behind schedule |
| Adviser feedback requires major revision | Medium | Medium | Submit drafts incrementally (per phase), not all at once at end |

---

## Assignment Legend

| Abbreviation | Name |
|-------------|------|
| JRP | John Ronald Pacaldo |
| CBA | Collin Brandon Asio |
| SFS | Simon France Sulibio |
