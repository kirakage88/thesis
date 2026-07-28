# Thesis Roadmap — Predictive Maintenance for Coiled Evaporators

Group: John Ronald Pacaldo · Collin Brandon Asio · Simon France Sulibio

**Architecture Decision:** Unsupervised anomaly detection (primary) \+ supervised classification (secondary, conditional). \[See appendix for full A vs B analysis.\]

---

## Legend

| Emoji | Type |
| :---- | :---- |
| 📝 | Paper Overhaul |
| 🔧 | Prototyping |
| 💻 | Coding |
| 🤖 | Machine Learning |
| 📊 | Data Collection |
| 🚀 | Deployment |
| 📋 | Documentation |

| Priority | Symbol |
| :---- | :---- |
| Critical | 🔴 |
| High | 🟠 |
| Medium | 🟡 |
| Low | 🟢 |

| Status | Symbol |
| :---- | :---- |
| Not started | ⬜ |
| In progress | 🔄 |
| Blocked | 🚫 |
| Completed | ✅ |

---

## Phase 1 — Paper Overhaul: Foundation

**Goal:** Rewrite Chapter 1 and pre-prototyping sections of Chapter 3 to reflect the reframed thesis: non-invasive anomaly detection as a complementary triage tool for scheduled preventive maintenance. Lock down the architecture before any hardware work.

### Chapter 1 — Introduction

- [x] 🔴 **Rewrite the thesis title** — `1.1 JOHN PACALDO`  
        
- [x] 🔴 **Rewrite the research gap** — `1.1 JOHN PACALDO`  
        
      \- \*\*Old:\*\* "No localized data-driven early warning exists; current maintenance is insufficient."    
        
      \- \*\*New:\*\* "Scheduled preventive maintenance ensures regular cleaning every 3–4 months, but the interval between services creates an information gap: maintenance staff cannot reliably identify which specific units are experiencing early-stage performance degradation between visits without physical disassembly. This study investigates whether a non-invasive sensor system — using only external temperature, electrical, and vibration measurements, with no evaporator access — can detect anomalous operating behavior, serving as a complementary triage tool to existing preventive maintenance at Xavier University. As Xavier University develops its Campus of the Future, this study serves as a proof-of-concept for site-specific, non-invasive AC condition monitoring."  
        
- [ ] 🔴 **Fix variable-sensor mapping** — `1.4 Conceptual Framework SIMON SULIBIO`  
        
      \- Remove: refrigerant leaks (no gas sensor), ice build-up (non-invasive access constraint), ESP32-CAM (cannot open evaporator)    
        
      \- Rename: "noise" → "vibration" (MPU6050 accelerometer)    
        
      \- Add: set temperature (manually recorded from thermostat/remote during each visit) — provides baseline for comparing actual vs. target cooling performance    
        
      \- Create explicit mapping table: Independent Variable → Sensor → Data Type → Model Input    
        
      \- Redraw conceptual framework diagram to match actual hardware and non-invasive approach  
        
- [ ] 🔴 **Add operational definition of Normal/Abnormal** — `1.1 / 3.1 COLLIN ASIO`  
        
      \- A unit is \*\*Normal\*\* if it exhibits acceptable cooling performance, no abnormal vibration or electrical behavior during inspection, and no maintenance concern is documented in the PPO maintenance logs.    
        
      \- A unit is \*\*Degraded\*\* if technician inspection identifies performance degradation, abnormal electrical or vibration characteristics, or a maintenance record documents a fault requiring corrective action.  
        
- [ ] 🔴 **Rewrite research questions for unsupervised focus** *`JOHN PACALDO`*  
        
      \- \*\*RQ1:\*\* Which non-invasive sensor measurements (supply-return temperature differential, compressor/fan current signatures, vibration spectral features) demonstrate the strongest discriminatory power for distinguishing normal from degraded unit behavior, as measured by feature importance and anomaly score separation?    
        
      \- \*\*RQ2:\*\* Which unsupervised anomaly detection model (Autoencoder, Isolation Forest, One-Class SVM, Gaussian Mixture Model) most reliably identifies AC units exhibiting anomalous operating signatures, validated through retrospective log comparison and controlled fault injection?    
        
      \- \*\*RQ3 (conditional):\*\* Does replacing raw environmental sensor features with a composite thermal comfort metric (PMV) improve anomaly detection sensitivity, provided the DIY airflow sensor is successfully developed?    
        
      \- \*\*RQ4:\*\* Does anomaly score generalize across AC units not seen during model development (unit-level evaluation), and does time-since-last-cleaning confound anomaly detection?  
        
- [ ] 🔴 **Rewrite hypotheses (falsifiable with margins and tests)** *`JOHN PACALDO`*  
        
      Each RQ has at least one hypothesis. Tests: Mann-Whitney U (p\<0.05) for group separation; paired bootstrap (p\<0.05) for feature contribution; TPR threshold for raw detection rate; within 3pp/5pp for performance margins; McNemar's (p\>0.05) for model equivalence; Spearman's ρ (p\>0.05) for confound correlation; ANOVA (p\>0.05) for kit-to-kit consistency.  
        
      \*\*RQ1 — Sensor measurement discriminatory power:\*\*  
        
      \- \*\*H1a:\*\* At least one sensor measurement group (supply-return temperature differential, compressor/fan current signatures, vibration spectral features) demonstrates statistically significant anomaly score separation between known-fault and known-healthy units (p \< 0.05, Mann-Whitney U test).  
        
      \- \*\*H1b:\*\* Vibration-derived features (spectrogram CNN output or statistical features) contribute statistically significant improvement to anomaly detection over temperature-and-electrical-only features (p \< 0.05, paired bootstrap).  
        
      \*\*RQ2 — Unsupervised model performance:\*\*  
        
      \- \*\*H2a:\*\* At least one unsupervised model (Autoencoder, Isolation Forest, One-Class SVM, Gaussian Mixture Model) achieves anomaly score separation between known-fault and known-healthy units (p \< 0.05, Mann-Whitney U test) AND true positive rate ≥ 80% on injected faults.  
        
      \- \*\*H2b:\*\* PCA-reduced features achieve anomaly detection performance within 3 percentage points of the full feature set AND show no statistically significant difference in unit-level anomaly ranking (p \> 0.05, McNemar's test).  
        
      \*\*RQ3 — Composite thermal comfort metric (conditional):\*\*  
        
      \- \*\*H3 (conditional):\*\* Replacing raw environmental sensor features with a single PMV composite metric does not significantly degrade anomaly detection performance (within 3pp of raw-feature baseline).  
        
      \*\*RQ4 — Generalization and confound verification:\*\*  
        
      \- \*\*H4a:\*\* Anomaly score separation on held-out units (Leave-One-Unit-Out evaluation) remains within 5 percentage points of in-sample performance (McNemar's test, p \> 0.05).  
        
      \- \*\*H4b:\*\* Time-since-last-cleaning and ambient environmental variables (temperature, humidity) show no statistically significant correlation with anomaly score (p \> 0.05, Spearman's ρ), and kit ID does not predict anomaly score (p \> 0.05, ANOVA).  
        
      \*\*Hypothesis Execution Order & Dependencies\*\* (for planning; draft stays in RQ reading order):  
        
      \*\*First to test — H1a (gate):\*\* If no sensor group separates known-fault from known-healthy, the entire sensor suite is in question. Test with a baseline model \+ Layer 1 retrospective data before investing in Phase 7 CNN / PCA / PMV.  
        
      | \# | H | Prerequisite | Earliest phase | Test |  
        
      |---|----|-------------|---------------|------|  
        
      | 1 | H1a | 1 trained baseline model \+ Layer 1 retrospective data (13 known-fault units from PPO logs) | Phase 8 start (or pilot in Phase 6\) | Mann-Whitney U, p\<0.05 |  
        
      | 2 | H2a (Mann-Whitney half) | All 4 models trained on known-fault scores (same data as H1a) | Phase 8, parallel with H1a | Mann-Whitney U, p\<0.05 |  
        
      | 3 | H2b | Best model trained on full \+ PCA-reduced features | Phase 8, after baseline trained | McNemar's p\>0.05 \+ within 3pp |  
        
      | 4 | H1b | Phase 7 vibration features ready (CNN or statistical) | Phase 8, after Phase 7 done | Paired bootstrap, p\<0.05 |  
        
      | 5 | H2a (TPR half) | Layer 2 fault injection data scored by trained models | Phase 8 Layer 2 | TPR ≥ 80% |  
        
      | 6 | H4a | Finalized model \+ Leave-One-Unit-Out loop | Phase 8 | McNemar's p\>0.05 \+ within 5pp |  
        
      | 7 | H4b | Anomaly scores \+ confound metadata (days-since-cleaning, ambient, kit ID) | Phase 8 Layer 4 | Spearman's ρ, ANOVA, p\>0.05 |  
        
      | 8 | H3 (conditional) | DIY airflow sensor built \+ PMV computed per trial | Phase 8, last | within 3pp (sensor fails → H3 dropped) |  
        
- [ ] 🔴 **Reframe positioning as complementary triage** — `1.1 COLLIN ASIO`  
        
      \- Explicitly state: this system does NOT replace scheduled preventive maintenance. It is a diagnostic layer that flags which units need attention between cleanings, helping the PPO prioritize inspections.    
        
      \- Reference the maintenance logs as evidence that faults have been observed between scheduled cleanings (e.g., "13-MAR-23 LEAK REPAIR & REPLACEMENT OF OUTDOOR FAN MOTOR").    
        
      \- Pitch as proof-of-concept for Campus of the Future implementation.  
        
- [ ] 🟠 **Strengthen RA 11285 rationale** — `1.1 SIMON SULIBIO`  
        
      \- Add quantified energy savings estimate: "30 units × avg 2.5kW × 2,000 hrs/yr × 6.4% fouling penalty (Niknami et al., 2024\\) × ₱12/kWh ≈ ₱115,000 annual waste. Early detection could reduce this."  
        
- [ ] 🟠 **Update scope and limitations for non-invasive approach** — `1.5 SIMON SUILBIO`  
        
      \- Scope: non-invasive external sensors only; 30-40 units across 3 locations; weekly visits with 2 portable kits (proof-of-concept phase); anomaly detection as triage tool. \*\*Long-term vision:\*\* permanent sensor module installed per AC unit (Campus of the Future), continuously monitoring with automated anomaly alerts — this thesis validates the core approach.    
        
      \- Acknowledge: cannot directly observe evaporator coil condition; model detects proxy signals, not faults themselves; weekly sampling may miss transient failures between visits; portable kit mounting introduces measurement variability (mitigated by standardized protocol \\+ kit ID tracking).    
        
      \- State explicitly: fault injection during validation is part of experimental design, not operational deployment. The deployed system remains non-invasive; invasive inspection is only for labeling during the study and for controlled fault injection.  
        
- [ ] 🟡 **Justify unsupervised over supervised** — `1.5 or 3.3 COLLIN ASIO`  
        
      \- Walk the reader through the data constraint: 13 known-problem units out of 2,599 campus-wide. In a 30-40 unit sample, expect 0-3 naturally occurring Abnormal observations. Supervised classification with 0-3 positive examples is statistically unvalidatable.    
        
      \- Unsupervised anomaly detection trains on abundant normal data (\\\~95%+ of data), learns the operating envelope, and flags deviations — matching the triage framing exactly.    
        
      \- Mention: supervised classification will be tested as a secondary experiment IF controlled fault injection produces enough labeled samples (30+).  
        
- [ ] 🟢 **Add scope diagram** — `1.5 SIMON SULIBIO`  
        
      \- Visual: in scope vs. out of scope. Non-invasive anomaly detection as focus.

### Chapter 3 — Methodology (Pre-Prototyping Sections)

- [ ] 🔴 **Clarify monitoring regime** — `3.1.1 COLLIN ASIO`  
        
      \- \*\*Weekly visits with 2 portable sensor kits.\*\* One location per day, rotating through 30-40 units across SBM-AVR, College of Engineering, and Faber Hall.    
        
      \- Each visit: 10 trials per unit. Each trial: 1 minute of continuous readings at 10 Hz \\= 600 samples/sensor/trial.    
        
      \- Rename "6-month monitoring" to "6-month study with weekly measurements" throughout.  
        
- [ ] 🔴 **Add sampling parameters table** — `3.1.5 COLLIN ASIO`  
        
      \- Per sensor: sampling rate (Hz), trial duration, readings per trial, total data per unit per visit.    
        
      \- BME280/DS18B20/ACS712/ZMPT101B: 10 Hz × 60s \\= 600 samples/trial × 9 sensors \\= 5,400 readings/unit/visit.    
        
      \- MPU6050: 100 Hz × 60s \\= 6,000 samples/trial → converted to spectrogram images.  
        
- [ ] 🔴 **Nested: 🔧 Hardware BOM finalization** — `3.1.4 COLLIN ASIO`  
        
      \- 2× Thermal Node kits: ESP32-C3 \\+ BME280 (I2C 0x76) \\+ 3× DS18B20 (OneWire GPIO10).    
        
      \- 2× Electrical/Vibration Node kits: ESP32-C3 \\+ 2× ACS712 \\+ ZMPT101B \\+ MPU6050.    
        
      \- 2× Master ESP32 (receiver, ESP-NOW → Serial).    
        
      \- 2× TFT display (ST7789 240×320, optional).    
        
      \- Per-unit cost estimate and sourcing plan.  
        
- [ ] 🔴 **Add unsupervised methodology justification** — `3.3 COLLIN ASIO`  
        
      \- Primary: 4 unsupervised models (Autoencoder, Isolation Forest, One-Class SVM, GMM).    
        
      \- Autoencoder: learns to reconstruct normal sensor readings; reconstruction error above threshold \\= anomaly.    
        
      \- Isolation Forest: isolates anomalous points efficiently; non-parametric, suited to mixed feature types.    
        
      \- One-Class SVM: learns decision boundary around normal data; kernel-based.    
        
      \- GMM: probabilistic model; likelihood scores for anomaly scoring.    
        
      \- Secondary (conditional): RF, XGBoost, RBF SVM if fault injection produces ≥30 labeled samples. Drop k-NN and DNN from primary lineup.  
        
- [ ] 🟠 **Add system architecture diagram** — `3.1.4 COLLIN ASIO`  
        
      \- 2 node types (Thermal \\+ Electrical/Vibration) → Master ESP32 (ESP-NOW) → Laptop/Server (Serial) → CSV → preprocessing pipeline.    
        
      \- No ESP32-CAM, no Frost Node, no Wi-Fi image upload.    
        
      \- Power source per node, communication paths, data flow.  
        
- [ ] 🟠 **Address ESP32-C3 ADC limitations** — `3.1.4 COLLIN ASIO`  
        
      \- Document ESP32-C3 ADC noise (ENOB \\\~9-10 bits) for ACS712 analog readings.    
        
      \- Mitigation: averaging 1,000+ samples per reading; consider external 16-bit ADC (ADS1115) if onboard proves insufficient. Acknowledge as limitation if using onboard ADC.  
        
- [ ] 🟠 **Define labeling and validation protocol** — `3.1.6 COLLIN ASIO`  
        
      \- \*\*Training (unsupervised):\*\* No labels needed. All sensor data used for training.    
        
      \- \*\*Validation (layered):\*\*    
        
        \- Layer 1: Retrospective comparison against 13 known-fault units from maintenance logs (deploy kit for 1-2 visits, check anomaly score separation). Mann-Whitney U test, p \\\< 0.05.    
        
        \- Layer 2: Controlled fault injection on 2-3 units (block return air, reduce refrigerant, misalign fan). Anomaly score must rise post-injection. Target ≥ 80% true positive rate.    
        
        \- Layer 3: Monthly technician spot-checks on 5-8 units. Correlate findings with anomaly scores. Target ≥ 70% agreement.    
        
        \- Layer 4: Confound verification — anomaly score must NOT be driven by weather, time-since-cleaning, or kit-to-kit variation.    
        
        \- Layer 5: Maintenance reset — if cleaned unit's anomaly score drops post-cleaning, strongest possible evidence of real signal.    
        
      \- \*\*Supervised secondary experiment (conditional):\*\* If fault injection yields ≥30 labeled samples, train RF/XGBoost/SVM. Report macro-F1. Use Group K-Fold (unit-level splits).  
        
- [ ] 🟡 **Add power management plan** — `3.1.4 COLLIN ASIO`  
        
      \- Power source per node (USB power bank, wall outlet, or AC unit tap).    
        
      \- Battery life estimate for portable operation.    
        
      \- Sleep/wake cycles if needed for energy optimization.  
        
- [ ] 🟡 **Define sensor failure protocol** — `3.1.5 COLLIN ASIO`  
        
      \- DS18B20 disconnect → flag row, continue remaining sensors, log error.    
        
      \- MPU6050 no reading → flag trial, attempt re-read, max 3 attempts.    
        
      \- Malformed readings → log, skip, alert.  
        
- [ ] 🟡 **Standardize portable kit mounting protocol** — `3.1.5 COLLIN ASIO`  
        
      \- Document exact probe placement per sensor type.    
        
      \- Include Kit ID as a model development feature (to detect kit-driven bias), exclude from final model.    
        
      \- Verify kit-to-kit calibration before each deployment day.  
        
- [ ] 🟡 **Add time-since-last-cleaning covariate** — `3.1.5 COLLIN ASIO`  
        
      \- Extract cleaning dates from PPO maintenance logs for each unit.    
        
      \- Compute days since last cleaning for each visit.    
        
      \- Include as model feature during development; test whether anomaly score is confounded by cleaning recency.

---

## Phase 2 — Prototyping: Hardware Validation

**Goal:** Assemble and test 2 complete portable sensor kits. Verify all sensors read correctly, ESP-NOW communication is stable, and the Master ESP32 outputs structured CSV data.

### Sensor Nodes

- [ ] 🔴 **🔧 Assemble Thermal Node prototype (×2)** — `ambient_module_final/`  
        
      \- ESP32-C3 \\+ BME280 (I2C 0x76) \\+ 3× DS18B20 (OneWire GPIO10).    
        
      \- Verify all 4 sensors read simultaneously.    
        
      \- Apply calibration factors as hardcoded constants.    
        
      \- Serial output: \`Temp=XX.X Hum=XX.X Counter=X A=XX.X B=XX.X C=XX.X\`.  
        
- [ ] 🔴 **🔧 Assemble Electrical/Vibration Node prototype (×2)**  
        
      \- ESP32-C3 \\+ 2× ACS712 \\+ ZMPT101B \\+ MPU6050.    
        
      \- Verify current and voltage readings with reference DMM at XU ME/EE labs.    
        
      \- Measure and record zero-current offset for both ACS712 channels.    
        
      \- Test MPU6050 vibration capture at 100 Hz; verify spectrogram conversion.  
        
- [ ] 🔴 **🔧 Verify MPU6050 calibration offsets**  
        
      \- From calibration CSV: AX\\\_BIAS \\= \\-0.005124, AY\\\_BIAS \\= \\-0.265409, AZ\\\_BIAS \\= 0.379842.    
        
      \- Apply in firmware as hardcoded constants.

### ESP-NOW Communication

- [ ] 🔴 **🔧 ESP-NOW master-slave pairing**  
        
      \- 2 senders (Thermal, Electrical/Vibration) → 1 Master ESP32.    
        
      \- Test channel scanning via SSID \`PLDTHOMEFIBRd2228\`; fallback channel 11\\.    
        
      \- Verify MAC addresses: Sender 1 \`E0:72:A1:72:22:94\`, Sender 2 \`E0:72:A1:72:29:00\`, Receiver \`E0:72:A1:6F:F8:6C\`.    
        
      \- Test 3-second send interval stability over 1-hour continuous run.    
        
      \- \*\*ESP-NOW receive callback must only set a flag\*\* (\`volatile bool newDataReady\`). Processing runs in \`loop()\` — never in ISR.  
        
- [ ] 🟠 **🔧 Timestamp synchronization protocol**  
        
      \- Master broadcasts sync pulse → both nodes timestamp readings.    
        
      \- Verify both nodes report same timestamp within ±50ms tolerance.  
        
- [ ] 🟡 **🔧 Data struct validation**  
        
      \- Verify \`EspNowPacket\` struct (type \\+ 6 floats) matches across all nodes.    
        
      \- Test edge cases: NaN values, sensor disconnect (default to 0.0 or \\-999.0).

### TFT Display UI (Optional)

- [ ] 🟡 **🔧 TFT complete UI** — `tft_complete/`  
      \- ST7789 240×320 SPI \+ XPT2046 touch.  
      \- Pages: Main Menu → Pairing → Devices → Units → System.  
      \- Display live sensor data from Master ESP32 via Serial/UART.

### Firmware Coding

- [ ] 🔴 **💻 Calibration factor integration**  
        
      \- Embed verified calibration constants in all sensor sketches:    
        
        \- BME280: \`T\_cal \= T\_raw × 1.0294412\`, \`H\_cal \= H\_raw × 1.0579399\`    
        
        \- DS18B20 A: \`1.701471 \+ 0.984997 × raw\`    
        
        \- DS18B20 B/C: \`1.637417 \+ 0.9783362 × raw\`    
        
        \- MPU6050: apply AX/AY/AZ bias offsets    
        
      \- ACS712: \`ADC\_raw − ADC\_Zero\_Offset\` → calibrated current via sensitivity factor.  
        
- [ ] 🟠 **💻 Data formatting script**  
        
      \- Master ESP32 outputs structured CSV line: \`timestamp,unit\_id,set\_temp,temp,humid,pressure,inlet,outlet,coil,comp\_current,fan\_current,voltage,accel\_x,accel\_y,accel\_z\`.    
        
      \- Ingest script: reads Serial, validates format and ranges, writes to \`02\_Data/raw/\` with naming convention: \`YYYYMMDDTHHmmSSZ\_\<Location\>\_\<UnitID\>\_\<TrialNum\>\_RAW.csv\`.

### Nested Paper Tasks

- [ ] 🟡 **📝 Update Chapter 3** from prototyping learnings  
      \- Record actual vs. expected sensor accuracy.  
      \- Document hardware substitutions and deviations from plan.  
      \- Update system architecture diagram with final wiring and confirmed sensor lineup.

---

## Phase 3 — Paper Overhaul: Literature & Gaps

**Goal:** Overhaul Chapter 2 (RRL) with a synthesis matrix, replacement of tangential studies, and alignment with the unsupervised anomaly detection methodology.

### Chapter 2 — Review of Related Literature

- [ ] 🔴 **📝 Add synthesis matrix** — `2.11 (new section)`  
        
      \- Multi-dimensional comparison table: Study | Model | Dataset size | Accuracy | Sensor types | HVAC type | Deployment context | Limitation.    
        
      \- Column for supervised vs. unsupervised approach.    
        
      \- Write 3-5 explicit research gaps this thesis addresses, including: "limited application of unsupervised anomaly detection in non-invasive HVAC condition monitoring using low-cost external sensors."  
        
- [ ] 🔴 **📝 Replace tangential studies**  
        
      \- Remove 2.8 (Aji et al., magnetic sensors — not HVAC).    
        
      \- Remove 2.9 (Abood et al., electromechanical motors — not HVAC).    
        
      \- Replace with:    
        
        \- Study on unsupervised anomaly detection for building/HVAC systems (expand Bouabdallaoui et al., 2021 — 2.5).    
        
        \- Study on low-cost sensor calibration for predictive maintenance.    
        
        \- Study on evaporator coil fouling detection via proxy signals (expand Niknami et al., 2024 — already cited in Chapter 1).  
        
- [ ] 🟠 **📝 Reconcile calibration formula with literature**  
        
      \- Fix Probe B regression output in Chapter 4: either update R output screenshot or correct stated formula. Verify all calibration formulas match firmware codebase exactly.    
        
      \- Fix Probe A data error (\`17.3\` → \`27.3\`) in appendix.  
        
- [ ] 🟡 **📝 Cite foundational ML papers**  
        
      \- Breiman (2001) for Random Forest. Chen & Guestrin (2016) for XGBoost. Cortes & Vapnik (1995) for SVM. Liu et al. (2008) for Isolation Forest. Schölkopf et al. (2001) for One-Class SVM.    
        
      \- Don't rely solely on Sarker (2021) for all algorithm descriptions.  
        
- [ ] 🟡 **📝 Add conceptual framework diagram from literature**  
        
      \- Visual: literature findings → informs this thesis architecture.    
        
      \- Highlight unique contribution: ESP32 \\+ ESP-NOW \\+ low-cost external sensors \\+ unsupervised anomaly detection as triage tool.

### Nested ML Tasks

- [ ] 🟠 **🤖 Final model selection with justification**  
      \- **Primary (unsupervised):** Autoencoder (deep learning; reconstruction error), Isolation Forest (tree-based; non-parametric; well-suited to small-medium data), One-Class SVM (kernel-based; comparison baseline), GMM (probabilistic; confidence scores).  
      \- **Secondary (supervised, conditional):** RF, XGBoost, RBF SVM — only if fault injection produces ≥30 labeled samples. Justification: supervised comparison experiment validates whether labeled data improves over unsupervised when labels are available.  
      \- **Dropped:** k-NN (rarely competitive at this sample size), DNN (insufficient training data — require hundreds to thousands of labeled examples), ESP32-CAM CNN (removed — non-invasive constraint).

---

## Phase 4 — Sensor Calibration: Remaining Sensors

**Goal:** Complete calibration of ACS712 and ZMPT101B sensors using equipment available at XU ME/EE labs. Build the calibration database for automated CCF application.

### ACS712 Current Calibration

- [ ] 🔴 **📊 Zero-offset calibration** — both ACS712 channels  
        
      \- Node powered on, no load connected.    
        
      \- 1,000 ADC readings over 60 seconds per sensor.    
        
      \- Compute: \`ADC\_Zero\_Offset \= mean(1,000 readings)\`.    
        
      \- Store per-sensor UID in calibration database (\`01\_Sensor\_Calibration/\`).  
        
- [ ] 🔴 **📊 Sensitivity (gain) calibration**  
        
      \- Connect known resistive loads: 50W, 200W, 250W bulbs.    
        
      \- Measure True-RMS current with reference DMM at XU ME/EE labs.    
        
      \- Linear regression per sensor: \`I\_actual \= m × (ADC\_raw − ADC\_Zero\_Offset) \+ c\`.    
        
      \- If non-linear at low currents (fan motor range 0-1A) → use piecewise or polynomial fit.

### ZMPT101B Voltage Calibration

- [ ] 🔴 **📊 Trimpot standardization**  
        
      \- Adjust onboard potentiometer: 250V input → ADC output \\\~640 (below saturation, provides headroom).    
        
      \- Standardize across both Electrical/Vibration Node kits.  
        
- [ ] 🔴 **📊 3rd-order polynomial calibration**  
        
      \- Variac: 10 voltage setpoints from 50V to 250V.    
        
      \- Record ADC reading vs. True-RMS DMM reference.    
        
      \- Fit 3rd-order polynomial per module: \`V\_actual \= a₀ \+ a₁·ADC \+ a₂·ADC² \+ a₃·ADC³\`.    
        
      \- Report R² and max absolute error.

### Calibration Database

- [ ] 🟠 **💻 Calibration database script**  
        
      \- JSON per sensor type: \`{UID: {type: "linear"|"polynomial", coefficients: \[...\]}}\`.    
        
      \- Version control in \`01\_Sensor\_Calibration/\`.    
        
      \- Python helper: \`apply\_ccf(uid, raw\_value) → calibrated\_value\`.  
        
- [ ] 🟡 **💻 Automated CCF application**  
        
      \- Preprocessing pipeline reads raw CSV → looks up UID → applies CCF → writes to \`02\_Data/interim/\`.    
        
      \- Unit test: known raw value → verify calibrated output matches expected.

### Nested Paper Tasks

- [ ] 🟠 **📝 Write Chapter 4 sensor calibration results**  
      \- Per sensor: scatter plot (sensor vs. reference with regression line \+ 95% CI band).  
      \- Per sensor: residual plot. Q-Q plot for residual normality.  
      \- Report R², RMSE, max error on held-out validation set (80/20 train/val split per sensor type).  
      \- Include uncertainty discussion: residual std error per sensor, whether accuracy is sufficient for anomaly detection.  
      \- Fix Probe A data error (`17.3` → `27.3`) before any analysis.  
      \- Reconcile Probe B formula (regression output must match stated formula in Ch4 and firmware).

---

## Phase 5 — Paper Overhaul: Methodology Details

**Goal:** Condense the \~40-page textbook content in Chapter 3.3. Replace supervised classification architectures with unsupervised anomaly detection model definitions. Define validation strategy in detail.

- [ ] 🔴 **📝 Condense Chapter 3.3 Model Development section**  
        
      \- Cut textbook content: move linear regression, gradient descent, backpropagation derivations to Appendix.    
        
      \- Keep in main text: 1-2 paragraph summary per model \\+ architecture specification table.  
        
- [ ] 🔴 **📝 Define unsupervised model architectures**  
        
      \- \*\*Autoencoder:\*\* Input (9 sensor features: set\\\_temp \\+ 8 calibrated sensor readings) → Encoder (Dense 64 ReLU → Dense 32 ReLU → Dense 16 latent) → Decoder (Dense 32 ReLU → Dense 64 ReLU → Dense 9 linear). Reconstruction error (MSE) as anomaly score. Threshold: 95th percentile of training reconstruction error.    
        
      \- \*\*Isolation Forest:\*\* n\\\_estimators \\\[100, 200, 500\\\], contamination \\\[auto, 0.01, 0.05, 0.10\\\], max\\\_samples \\\[256, auto\\\]. Anomaly score: path length.    
        
      \- \*\*One-Class SVM:\*\* kernel \\\[RBF\\\], nu \\\[0.01, 0.05, 0.10\\\], gamma \\\[scale, auto, 0.01, 0.1\\\]. Anomaly score: signed distance from decision boundary.    
        
      \- \*\*GMM:\*\* n\\\_components \\\[1, 2, 3, 5, 10\\\] (selected via BIC). Anomaly score: negative log-likelihood.  
        
- [ ] 🔴 **📝 Define CNN spectrogram anomaly detection architecture**  
        
      \- Input: MPU6050 vibration → spectrogram image (time-frequency representation).    
        
      \- Architecture: Transfer learning (MobileNetV2 pretrained on ImageNet), fine-tuned on vibration spectrograms.    
        
      \- Approach: Convolutional Autoencoder — learns to reconstruct spectrograms of normal vibration patterns. Reconstruction error above threshold \\= anomalous vibration.    
        
      \- Vibration anomaly score → concatenated with sensor features in final anomaly model OR used as a multimodal anomaly detection branch.    
        
      \- Explicitly justify ImageNet weights: not an external HVAC dataset — a general-purpose computer vision foundation model, which is standard practice.  
        
- [ ] 🟠 **📝 Specify hyperparameter search space** per model  
        
      \- Isolation Forest: n\\\_estimators \\\[100, 200, 500\\\], contamination \\\[0.01, 0.05, 0.10\\\].    
        
      \- One-Class SVM: nu \\\[0.01, 0.05, 0.10\\\], gamma \\\[scale, auto, 0.01, 0.1\\\].    
        
      \- GMM: n\\\_components \\\[1, 2, 3, 5, 10\\\], covariance\\\_type \\\[full, tied, diag, spherical\\\].    
        
      \- Autoencoder: latent\\\_dim \\\[8, 16, 32\\\], learning\\\_rate \\\[0.001, 0.0001\\\], epochs \\\[50, 100\\\], batch\\\_size \\\[32, 64\\\].  
        
- [ ] 🟡 **📝 Add overfitting mitigation section**  
        
      \- Autoencoder: L2 regularization, dropout in encoder, early stopping (patience=10).    
        
      \- Isolation Forest: max\\\_samples, limited tree depth.    
        
      \- One-Class SVM: nu parameter controls outlier fraction.    
        
      \- GMM: BIC for model selection.  
        
- [ ] 🟡 **📝 Define evaluation metrics for unsupervised models** — map to H1a–H4b  
        
      \- \*\*H1a \+ H2a-MW:\*\* Anomaly score separation (known-fault vs. known-healthy): Mann-Whitney U test, p\<0.05.    
        
      \- \*\*H1b:\*\* Vibration feature contribution: paired bootstrap, p\<0.05.    
        
      \- \*\*H2a-TPR:\*\* True positive rate on injected faults: ≥ 80%. False positive rate on known-healthy: ≤ 15%.    
        
      \- \*\*H2b:\*\* PCA parity: within 3pp \+ McNemar's p\>0.05.    
        
      \- \*\*H3 (conditional):\*\* PMV parity: within 3pp.    
        
      \- \*\*H4a:\*\* Unit-level generalization: within 5pp \+ McNemar's p\>0.05.    
        
      \- \*\*H4b:\*\* Confound verification: Spearman's ρ p\>0.05 (ambient, cleaning), ANOVA p\>0.05 (kit, location).    
        
      \- Precision@K and Recall@K for ranked anomaly lists (operational triage metrics).

### Nested Coding Tasks

- [ ] 🟡 **💻 Python environment setup**  
        
      \- Activate venv: \`cd "codes/python/machine learning"; python \-m venv .venv; .venv\\Scripts\\Activate.ps1\`.    
        
      \- Install deps: \`pip install \-r ../requirements.txt\`.    
        
      \- Verify: \`python \-c "import numpy, matplotlib, sklearn, pandas, torch; print('OK')"\`.  
        
- [ ] 🟡 **💻 Project scaffolding**  
        
      \- Create \`03\_Code/\` directory structure (ingest, preprocessing, modeling, evaluation subdirs).    
        
      \- Initialize Git for code tracking.    
        
      \- Create \`config.yaml\` for paths, parameters, model configs, anomaly thresholds.

---

## Phase 6 — Data Collection

**Goal:** Deploy 2 portable kits across 30-40 units at 3 locations over 6 months. Collect consistent, calibrated sensor data. Apply weekly labeling protocol for validation.

### Hardware Deployment

- [ ] 🔴 **📊 Finalize 30-40 unit sample**  
        
      \- Select units from SBM-AVR, College of Engineering, Faber Hall 1st floor.    
        
      \- Prioritize units with "With Concern" status from maintenance logs to maximize abnormal data.    
        
      \- Prioritize split-type units (CM, CT, WM types) over window-type (WRAC).    
        
      \- Pull cleaning dates from PPO maintenance logs for each selected unit.  
        
- [ ] 🔴 **📊 Weekly data collection sessions** — 6 months  
        
      \- 2 kits, one location per day, rotate through all units.    
        
      \- Each visit: 10 trials per unit.    
        
      \- Each trial: 1 minute of continuous readings at 10 Hz (sensors) \\+ 100 Hz (MPU6050).    
        
      \- Record per trial: set temperature (manually read from thermostat/remote), ambient temp, humidity, pressure, inlet/outlet/coil temp, compressor/fan current, supply voltage, 3-axis acceleration.    
        
      \- Compute time-since-last-cleaning per unit per visit from maintenance logs.  
        
- [ ] 🟠 **📊 Controlled fault injection validation** — 3 sessions during study  
        
      \- With campus facilities permission, induce controlled faults on 2-3 units per session:    
        
        \- Partially block return air grille (simulate fouling/obstruction).    
        
        \- Reduce refrigerant charge via service valve (requires licensed technician — one-time supervised procedure).    
        
        \- Misalign fan blade (simulate mechanical imbalance).    
        
      \- Protocol: baseline measurement → induce fault → post-fault measurement → restore → recovery measurement.    
        
      \- Label each phase explicitly. This creates known ground truth for model validation.  
        
- [ ] 🟠 **📊 Monthly technician spot-checks** — validation layer  
        
      \- Rotating subset: 5-8 units per month.    
        
      \- Brief visual inspection checklist: abnormal vibration, poor cooling, unusual current, excessive noise, visible external issues.    
        
      \- Record findings. Correlate with anomaly scores at end of study.

### Data Pipeline

- [ ] 🔴 **💻 Data ingestion script**  
        
      \- Reads Serial from Master ESP32.    
        
      \- Validates format (expected columns, ranges).    
        
      \- Writes to \`02\_Data/raw/\` with naming convention: \`YYYYMMDDTHHmmSSZ\_\<Location\>\_\<UnitID\>\_\<TrialNum\>\_RAW.csv\`.  
        
- [ ] 🟠 **💻 Data cleaning & CCF application**  
        
      \- Script reads \`02\_Data/raw/\` → applies CCFs from \`01\_Sensor\_Calibration/\` → validates ranges → writes to \`02\_Data/interim/\`.    
        
      \- Handles missing values: forward-fill short gaps (\\\< 5 readings), flag longer gaps with indicator column.    
        
      \- Detects and flags outliers (outside 3σ or manual engineering thresholds).  
        
- [ ] 🟠 **💻 Feature engineering** for interim → processed  
        
      \- Rolling window statistics per trial: mean, std, min, max, slope.    
        
      \- Rate-of-change features: Δ(Inlet−Outlet)/Δt, ΔCoilTemp/Δt.    
        
      \- Derived COP proxy: (Inlet − Outlet) / Compressor Current.    
        
      \- Derived target delta-T: (Set Temp − Outlet Temp) — positive delta indicates AC is meeting target; negative delta indicates degradation.    
        
      \- Vibration statistical features: RMS, peak amplitude, spectral kurtosis, dominant frequency.    
        
      \- Vibration spectrogram generation: FFT → time-frequency image saved per trial.    
        
      \- Time-since-last-cleaning: computed from maintenance log cleaning dates.    
        
      \- Kit ID: included during development, excluded from final model.  
        
- [ ] 🟡 **💻 Data validation dashboard** (optional)  
        
      \- Simple Streamlit page: per-unit data completeness, sensor health, weekly trial count.    
        
      \- Alerts if unit has \\\< 10 trials in a week.

### Nested Paper Tasks

- [ ] 🟡 **📝 Update Chapter 3 DMP section**  
      \- Replace theoretical DMP with actual implementation notes.  
      \- Record deviations from planned storage/backup strategy.  
      \- Document actual file counts and data volumes.

---

## Phase 7 — Machine Learning: Vibration CNN

**Goal:** Train a convolutional autoencoder on MPU6050 vibration spectrograms to detect anomalous vibration patterns. This output feeds into the main unsupervised anomaly detection models.

- [ ] 🔴 **🤖 Generate vibration spectrogram dataset**  
        
      \- Per trial: MPU6050 100 Hz × 60s \\= 6,000 samples → FFT spectrogram image.    
        
      \- \\\~240 spectrograms per unit over 6 months (24 visits × 10 trials). 35 units × 240 ≈ 8,400 spectrograms total.    
        
      \- Organize: train on normal-condition units (majority), validate on known-fault \\+ injected-fault units.  
        
- [ ] 🔴 **🤖 Train convolutional autoencoder**  
        
      \- Architecture: MobileNetV2 encoder (pretrained ImageNet weights) → latent bottleneck → decoder.    
        
      \- Loss: MSE reconstruction error.    
        
      \- Save best model (lowest val\\\_loss) as \`cnn\_vibration\_autoencoder.pth\`.    
        
      \- Output per spectrogram: reconstruction error (anomaly score) \\+ latent feature vector.  
        
- [ ] 🟠 **🤖 Vibration anomaly detection evaluation** *(feeds H1b)*  
        
      \- Test on injected-fault units: reconstruction error must increase significantly post-fault vs. pre-fault.    
        
      \- Test on known-fault units from maintenance logs: reconstruction error should be higher than fleet average.    
        
      \- Report: true positive rate on injected faults, anomaly score separation (Mann-Whitney U).  
        
      \- Output ready for Phase 8 H1b ablation: CNN reconstruction error \+ latent vector extracted per trial.  
        
- [ ] 🟡 **🤖 Ablation study** (if time permits)  
        
      \- Compare: pretrained MobileNetV2 encoder vs. custom CNN from scratch.    
        
      \- Compare: reconstruction error vs. latent feature vector as anomaly score.    
        
      \- Compare: spectrogram resolution (frequency bins, time windows).

### Nested Paper Tasks

- [ ] 🟠 **📝 Write Chapter 4 vibration CNN results**  
      \- Report: architecture, dataset size, training curves (loss over epochs), anomaly score distributions.  
      \- Include: sample spectrograms (normal vs. anomalous with reconstruction overlay), anomaly score distributions for known-fault vs. healthy units.

---

## Phase 8 — Machine Learning: Unsupervised Anomaly Detection

**Goal:** Train and evaluate the 4 unsupervised models on full sensor \+ vibration feature set. Compare performance. Run the conditional supervised secondary experiment if fault injection yields enough labeled data.

### Preprocessing Pipeline

- [ ] 🔴 **🤖 Complete preprocessing pipeline**  
        
      \- Implementation in \`03\_Code/2\_preprocessing/\`.    
        
      \- Features: set\\\_temp \\+ 8 calibrated sensor readings \\+ vibration anomaly score from CNN \\+ vibration statistical features (RMS, kurtosis, peak frequency) \\+ time-since-last-cleaning.    
        
      \- Standardization: fit on normal-condition units only, transform all data.    
        
      \- PCA: fit on normal-condition units; plot variance explained; select k with ≥ 95% cumulative variance.    
        
      \- Output: X\\\_all, metadata (unit\\\_id, timestamp, kit\\\_id, location) saved to \`02\_Data/processed/\`.  
        
- [ ] 🟠 **🤖 Feature importance analysis**  
        
      \- Univariate Mann-Whitney U: which features differentiate known-fault from known-healthy units.    
        
      \- Permutation importance (using Isolation Forest as reference model).    
        
      \- Report: top 5 most discriminative features, effect sizes, p-values.

### Model Training

- [ ] 🔴 **🤖 Train Isolation Forest**  
        
      \- Hyperparameter tuning via grid search (contamination, n\\\_estimators, max\\\_samples).    
        
      \- Save \`isolation\_forest.pkl\`.    
        
      \- Feature importance: which features drive isolation.  
        
- [ ] 🔴 **🤖 Train One-Class SVM**  
        
      \- Hyperparameter tuning via grid search (nu, gamma, kernel).    
        
      \- Scale features before training (SVM is distance-sensitive).    
        
      \- Save \`one\_class\_svm.pkl\`.  
        
- [ ] 🔴 **🤖 Train Gaussian Mixture Model**  
        
      \- Select n\\\_components via BIC (test 1-10 components).    
        
      \- Save \`gmm.pkl\`.    
        
      \- Report: per-component means (interpretable "normal operating modes").  
        
- [ ] 🔴 **🤖 Train Autoencoder**  
        
      \- PyTorch implementation.    
        
      \- Architecture per Phase 5 definition.    
        
      \- Early stopping (patience=10 on validation reconstruction loss).    
        
      \- Save \`autoencoder.pth\`.

### Model Evaluation

- [ ] 🔴 **🤖 Layer 1 — Retrospective log validation** *(H1a \+ H2a-MW)*  
        
      \- Deploy kit to known-fault units (1-2 visits each).    
        
      \- \*\*H1a:\*\* Anomaly score separation per sensor measurement group (supply-return temp differential, compressor/fan current signatures, vibration spectral features) between known-fault and known-healthy units. Mann-Whitney U, p \\\< 0.05.  
        
      \- \*\*H2a-MW:\*\* All 4 models tested for anomaly score separation between known-fault and known-healthy units. Mann-Whitney U, p \\\< 0.05.  
        
      \- Report: mean anomaly score per group, effect size (Cohen's d).  
        
- [ ] 🔴 **🤖 H2b — PCA parity test**  
        
      \- Train best model on full features and on PCA-reduced features (k components with ≥ 95% cumulative variance).    
        
      \- Compare: |TPR\_full − TPR\_PCA| ≤ 3 percentage points.    
        
      \- McNemar's test on binary classification outcomes (above/below threshold): p \\\> 0.05 → no significant difference → PCA is viable.    
        
- [ ] 🟠 **🤖 H1b — Vibration ablation (paired bootstrap)**  
        
      \- Requires Phase 7 vibration features (CNN reconstruction error \+ latent vector, or statistical: RMS, kurtosis, peak frequency).    
        
      \- Train two model variants of the best model: temperature+electrical only vs. temperature+electrical+vibration. Same hyperparameters.    
        
      \- Compute performance metric (AUC or TPR) on held-out validation set for both variants.    
        
      \- Paired bootstrap (1,000+ resamples): compute performance gap per resample. If 95%+ of gaps \\\> 0 → p \\\< 0.05 → vibration contributes significantly.    
        
- [ ] 🔴 **🤖 Layer 2 — Controlled fault injection validation** *(H2a-TPR)*  
        
      \- Run all 4 models on pre-fault → post-fault → recovery data.    
        
      \- \*\*H2a-TPR:\*\* Anomaly score must rise post-injection for each fault type. True positive rate ≥ 80% across injected faults.    
        
      \- False positive rate on known-healthy fleet ≤ 15%.  
        
- [ ] 🔴 **🤖 Layer 4 — Confound verification** *(H4b)*  
        
      \- Assemble per-unit metadata: anomaly score, time-since-last-cleaning, ambient temp, ambient humidity, kit ID, location.    
        
      \- \*\*Spearman's ρ:\*\* anomaly score vs. days-since-cleaning, ambient temp, ambient humidity. All p \\\> 0.05 → no correlation.    
        
      \- \*\*ANOVA:\*\* anomaly score across kit IDs and locations. p \\\> 0.05 → no kit/location bias.    
        
      \- If any confound correlates → include it as a model feature, retrain, report both (with and without).  
        
- [ ] 🟠 **🤖 Layer 3 — Technician agreement**  
        
      \- Monthly spot-check findings vs. anomaly scores.    
        
      \- Report: agreement rate, Cohen's Kappa.  
        
- [ ] 🟠 **🤖 Layer 5 — Maintenance reset**  
        
      \- For units cleaned mid-study: anomaly score pre-cleaning vs. post-cleaning.    
        
      \- Expect: significant drop post-cleaning.    
        
      \- Report: paired t-test or Wilcoxon signed-rank.  
        
- [ ] 🟠 **🤖 Model comparison** *(answers H2a — which model wins?)*  
        
      \- Comparison table: Isolation Forest vs. One-Class SVM vs. GMM vs. Autoencoder.    
        
      \- Metrics: TPR on injected faults, FPR on healthy fleet, anomaly score separation (effect size), agreement with technician.    
        
      \- Ranking: which model performs best overall? Report per H2a: at least one must achieve p\<0.05 (Mann-Whitney) AND TPR ≥80%.  
        
- [ ] 🟠 **🤖 H4a — Unit-level generalization (Leave-One-Unit-Out)**  
        
      \- LOUO evaluation: for each unit U, train on all other units, score U. Repeat for all units.    
        
      \- Compare TPR (or AUC) on held-out units vs. in-sample units: |performance gap| ≤ 5 percentage points.    
        
      \- McNemar's test comparing in-sample vs. held-out binary outcomes: p \\\> 0.05 → no significant difference → model generalizes.    
        
      \- Report: does performance degrade significantly vs. random split? If yes → model is learning unit identities, not fault signatures.  
        
- [ ] 🟡 **🤖 H3 (conditional) — PMV composite metric comparison**  
        
      \- Requires: DIY airflow sensor built and functional. If sensor fails → H3 and RQ3 silently dropped.    
        
      \- Compute PMV per trial (temp, humidity, airflow, radiant temp).    
        
      \- Train model on PMV-only features vs. raw environmental features. Best model from comparison.    
        
      \- Compare TPR/AUC: |performance\_gap| ≤ 3 percentage points → PMV is a viable alternative.  

### Conditional Secondary: Supervised Classification

- [ ] 🟡 **🤖 IF fault injection yields ≥ 30 labeled samples**  
      \- Train: RF, XGBoost, RBF SVM on labeled subset (fault-injected \+ known-fault \+ known-healthy).  
      \- Split: Group K-Fold by unit ID (all readings from one unit in same fold).  
      \- Report: macro-F1, per-class precision/recall, confusion matrix.  
      \- Compare: does supervised classification with labels outperform unsupervised anomaly detection? If yes → strong evidence for labeled-data value. If no → unsupervised is genuinely better for this problem.  
      \- **Do NOT** run if \< 30 labeled samples; this experiment is conditional and its absence is documented.

### Nested Paper Tasks

- [ ] 🟠 **📝 Write Chapter 4 anomaly detection results**  
      \- Per hypothesis: statistical test results, effect sizes, p-values (H1a, H1b, H2a, H2b, H3-if-conditional, H4a, H4b).  
      \- Per layer: validation results table summarizing which hypotheses were tested by which layer.  
      \- Model comparison table with all metrics.  
      \- Confound verification: Spearman's ρ results, ANOVA results.  
      \- Feature importance: top discriminative sensor readings.  
      \- Interpretation: which model is recommended and why.

---

## Phase 9 — Deployment

**Goal:** Build the Streamlit dashboard and automated anomaly scoring pipeline. Deploy on the Ingest Server for live use during the final month of the study.

> **Note:** Current deployment (thesis) uses a single ingest server with manual weekly data collection via portable kits. The long-term vision (Campus of the Future) is a permanently-installed sensor module per AC unit streaming continuously to a centralized server.

### Server Setup

- [ ] 🔴 **🚀 Ingest Server configuration**  
        
      \- Set up dedicated PC or laptop with Python environment.    
        
      \- Configure Wi-Fi network (same as Master ESP32).    
        
      \- Install: Python 3.11+, watchdog, streamlit, joblib, pandas, numpy, scikit-learn, pytorch, sqlite3.    
        
      \- Set up directory structure from DMP.  
        
- [ ] 🔴 **💻 Ingest service script**  
        
      \- Reads Serial from Master ESP32.    
        
      \- Validates and writes to \`02\_Data/raw/\`.    
        
      \- Runs as persistent background process.

### Anomaly Scoring Pipeline

- [ ] 🔴 **🚀 Watchdog automation setup**  
        
      \- Monitor \`02\_Data/raw/\` for new files (use staging directory \\+ atomic move to prevent race conditions).    
        
      \- Trigger on new complete CSV → load → apply CCFs → preprocess → load best model → compute anomaly score → store result.  
        
- [ ] 🔴 **💻 Automated anomaly scoring script**  
        
      \- Load best model (e.g., \`isolation\_forest.pkl\`).    
        
      \- Load scaler \\+ PCA transformer (fit during Phase 8).    
        
      \- Process: set\\\_temp \\+ 8 sensor readings → calibrated → standardized → PCA → model.anomaly\\\_score().    
        
      \- Store: \`{unit\_id, timestamp, anomaly\_score, sensor\_snapshot}\` → \`anomalies.db\`.    
        
      \- Error handling: catch NaN, malformed input, shape mismatch → log error → skip file.  
        
- [ ] 🟠 **🚀 SQLite anomalies database**  
        
      \- Schema: \`anomalies\` table (id, unit\\\_id, timestamp, anomaly\\\_score, model\\\_name, sensor\\\_json).    
        
      \- Schema: \`alerts\` table (id, unit\\\_id, timestamp, severity, anomaly\\\_score\\\_threshold\\\_exceeded, acknowledged).    
        
      \- Create indexes on unit\\\_id, timestamp for query performance.  
        
- [ ] 🟡 **💻 Alert threshold logic**  
        
      \- Anomaly score in top 5% of training distribution → warning.    
        
      \- Anomaly score in top 1% → alert.    
        
      \- 3 consecutive alerts for same unit → critical (flag for immediate inspection).    
        
      \- Configurable via \`config.yaml\`.

### Dashboard

- [ ] 🟠 **🚀 Streamlit dashboard — main status page**  
        
      \- \`app.py\` with overview: all 30-40 units, most recent anomaly score each.    
        
      \- Color-coded grid: 🟢 Normal (below 95th percentile) / 🟠 Warning (95-99th) / 🔴 Alert (above 99th).    
        
      \- Auto-refresh every 30 seconds or triggered by watchdog file event.  
        
- [ ] 🟠 **🚀 Streamlit dashboard — unit detail page**  
        
      \- Dropdown: select unit by ID.    
        
      \- Historical chart: sensor time-series (temp, current, voltage) \\+ anomaly score overlay.    
        
      \- Anomaly history: date → anomaly score → alert status.    
        
      \- Time-since-last-cleaning indicator.  
        
- [ ] 🟡 **🚀 Streamlit dashboard — admin page**  
        
      \- Model retraining trigger button.    
        
      \- Data collection status (units not visited this week).    
        
      \- Alert acknowledgment UI.  
        
- [ ] 🟡 **💻 Streamlit authentication** (optional)  
        
      \- Simple password protection via environment variable or config.    
        
      \- Read-only view for maintenance staff, admin view for researchers.

### Cloud Sync (Optional)

- [ ] 🟢 **🚀 Supabase cloud backup**  
      \- Nightly sync script: `anomalies.db` → Supabase.  
      \- Ensure API key is NOT stored in plaintext (use environment variable).

### Nested Paper Tasks

- [ ] 🟠 **📝 Finalize Chapter 3 deployment section**  
      \- Replace theoretical deployment plan with implementation summary.  
      \- Include: architecture diagram, technology choices, deployment workflow.  
      \- Add dashboard screenshots in Appendix.

---

## Phase 10 — Finalization

**Goal:** Complete all writing, integrate results, format for submission, and prepare defense.

### Chapter 4 — Complete Results & Discussion

- [ ] 🔴 **📝 Integrate all Chapter 4 subsections**  
        
      \- 4.1 Sensor calibration (BME280, DS18B20, ACS712, ZMPT101B).    
        
      \- 4.2 Vibration CNN spectrogram anomaly detection results.    
        
      \- 4.3 Dataset overview (feature statistics, PCA results, unit-level distributions, time-since-cleaning profiles).    
        
      \- 4.4 Unsupervised anomaly detection results — all 4 models.    
        
      \- 4.5 Validation layer results (retrospective logs, fault injection, technician agreement, confound checks, maintenance reset).    
        
      \- 4.6 Conditional supervised classification results (if applicable).    
        
      \- 4.7 Deployment results (dashboard screenshots, anomaly scoring latency, system uptime).  
        
- [ ] 🔴 **📝 Discussion per section**  
        
      \- Why did model X outperform model Y? Link back to literature.    
        
      \- Were the hypotheses supported? (H1a–H4b: 7 hypotheses, each with statistical test results).    
        
      \- How did the 4-layer validation strategy perform — which layers provided strongest evidence?    
        
      \- Limitations encountered (sensor noise, dataset size, sparse known-fault units, ambient confounds).    
        
      \- Implications for Xavier University maintenance practices and Campus of the Future.

### Chapter 5 — Conclusion & Recommendations

- [ ] 🟠 **📝 Write conclusions**  
        
      \- Summary of what was built and tested.    
        
      \- Answer each research question directly.    
        
      \- Key finding: which model is recommended and why.  
        
- [ ] 🟠 **📝 Write recommendations**  
        
      \- For Xavier University PPO: adopt anomaly detection as triage tool, integrate with existing quarterly maintenance cycle. Transition from portable proof-of-concept to permanent per-unit sensor modules (weatherproof enclosure, AC-powered, fixed mounting brackets, automated calibration, remote firmware updates).    
        
      \- For future research: multi-fault type classification, permanent sensor installation, regression-based degradation forecasting, mobile app, expansion to all 2,599 campus units.    
        
      \- For hardware: external ADC for ACS712, permanent mounting brackets, automated calibration protocol.

### Final Deliverables

- [ ] 🟠 **📝 Abstract** — 250-300 words.  
- [ ] 🟡 **📝 Acknowledgements**.  
- [ ] 🟡 **📝 Appendices** — calibration data tables, R regression outputs, full code listings, dashboard screenshots, maintenance log excerpts, fault injection protocols.  
- [ ] 🟡 **📋 APA/citation audit** — check all in-text citations → reference list, consistent format throughout.  
- [ ] 🟡 **📋 Table of Contents, List of Figures, List of Tables** — auto-generated.  
- [ ] 🟡 **📋 Defense presentation** — 15-20 slides.  
      \- Problem & motivation: the information gap between cleanings.  
      \- Architecture: non-invasive → 2 portable kits → ESP-NOW → anomaly detection (proof-of-concept for permanent per-unit modules on Campus of the Future).  
      \- Methodology: why unsupervised? (walk through the 13-in-2,599 math).  
      \- Key results (1 slide per major finding).  
      \- Validation: the 4-layer evidence.  
      \- Conclusions & recommendations.  
      \- Demo video of dashboard (1-2 min).

---

## Milestones & Deadlines

| Date | Milestone | Deliverables |
| :---- | :---- | :---- |
| YYYY-MM-DD | Phase 1 complete | Ch1 overhauled, Ch3 pre-proto sections, architecture locked |
| YYYY-MM-DD | Phase 2 complete | 2 portable kits assembled, ESP-NOW working, CSV output verified |
| YYYY-MM-DD | Phase 3 complete | Ch2 overhauled, synthesis matrix, literature aligned with unsupervised |
| YYYY-MM-DD | Phase 4 complete | ACS712 \+ ZMPT101B calibrated, calibration DB built, Ch4 calibration section drafted |
| YYYY-MM-DD | Phase 5 complete | Ch3 model dev section condensed, 4 unsupervised architectures defined, validation protocol documented |
| YYYY-MM-DD | Phase 6 complete | 6-month data collection, 30-40 units, fault injection sessions, technician spot-checks |
| YYYY-MM-DD | Phase 7 complete | CNN vibration autoencoder trained, evaluated, Ch4 vibration results written |
| YYYY-MM-DD | Phase 8 complete | 4 unsupervised models trained \+ evaluated, all 5 validation layers, Ch4 anomaly results written |
| YYYY-MM-DD | Phase 9 complete | Dashboard live, anomaly scoring pipeline running, Ch3 deployment finalized |
| YYYY-MM-DD | Phase 10 complete | Full thesis draft submitted for adviser review |
| YYYY-MM-DD | Defense | Presentation, demo, Q\&A |
| YYYY-MM-DD | Final submission | Hardbound copies \+ digital archive |

---

## Risk Registry

| Risk | Likelihood | Impact | Mitigation |
| :---- | :---- | :---- | :---- |
| Insufficient Abnormal data (0-3 natural faults in 6 months) | High | High | **Already mitigated** — unsupervised approach does not need Abnormal labels for training. Fault injection provides guaranteed Abnormal samples for validation. |
| Fault injection permission denied by campus facilities | Medium | High | Engage PPO early (Phase 1). Present as research collaboration, not liability. Have adviser endorse. If denied: rely on retrospective log validation \+ technician spot-checks only. |
| Calibration equipment not available at XU labs | Low | High | **Confirmed available.** Verify specific equipment access during Phase 1\. |
| DIY airflow sensor not ready in time (PMV experiment) | High | Low | **Already mitigated** — PMV is conditional. If sensor fails, H3 and RQ3 drop silently. Does not affect primary thesis contribution. |
| 30-40 units overwhelming for 2-kit weekly rotation | Medium | Medium | Start with smaller rotation (20 units), expand as process stabilizes. Document scaling challenges honestly. |
| Scope too large for 3 members | Medium | High | Cut non-critical tasks (Supabase cloud sync, TFT UI, Streamlit auth) if behind schedule. Supervised secondary experiment is conditional — drop without penalty if insufficient data. |
| Adviser feedback requires major revision | Medium | Medium | Submit drafts incrementally per phase, not all at once at end. Each phase produces a reviewable deliverable. |
| Anomaly score confounded by ambient conditions | Medium | Medium | **Mitigated by Layer 4 validation.** Include ambient temp/humidity/time-since-cleaning as control variables. Report confound checks transparently. |
| CNN spectrogram approach fails (data volume, domain mismatch) | Medium | Medium | **Fallback:** vibration statistical features (RMS, kurtosis, peak frequency) as tabular features. CNN is attempted but not required for thesis success. |

---

## Assignment Legend

| Abbreviation | Name |
| :---- | :---- |
| JRP | John Ronald Pacaldo |
| CBA | Collin Brandon Asio |
| SFS | Simon France Sulibio |

---

## Appendix: Supervised vs. Unsupervised Decision Summary

**Three LLMs independently reviewed the methodology choice. Verdict: 3-0 for Unsupervised Anomaly Detection.**

### Why Unsupervised Won

| Reason | Detail |
| :---- | :---- |
| **Math is fatal for supervised** | 13 known-problem units / 2,599 campus-wide. 0-3 Abnormal observations expected in 30-40 unit study sample. Supervised classification with 0-3 positive examples is statistically unvalidatable. |
| **Labels aren't ground truth** | Technician visual inspection is a subjective proxy — cannot see the evaporator (non-invasive). Training supervised on proxy labels \= training to reproduce noise. |
| **Matches the thesis claim** | "Flag unusual behavior → prioritize inspection" is anomaly detection, not classification. The words match the method. |
| **Handles novel failures** | Unsupervised detects ANY deviation from normal. Supervised can only detect failure modes present in training data. |

### Supervised as Conditional Secondary

If controlled fault injection produces ≥ 30 labeled Abnormal samples, run supervised classifiers (RF, XGBoost, RBF SVM) as a **comparison experiment**. This is a bonus, not a dependency. If it fails or insufficient data is produced, the unsupervised primary contribution stands alone.

### Validation Strategy

5-layer validation designed to answer "how do you prove it works without labels?":

1. **Retrospective log comparison** — anomaly score separation between known-fault and known-healthy units (Mann-Whitney U, p \< 0.05).  
2. **Controlled fault injection** — inject known faults, verify anomaly score rises (TPR ≥ 80%).  
3. **Monthly technician spot-checks** — correlate findings with anomaly scores (agreement ≥ 70%).  
4. **Confound verification** — prove anomaly score isn't driven by weather, cleaning recency, or kit variation.  
5. **Maintenance reset** — cleaned units show anomaly score drop → real signal, not noise.
