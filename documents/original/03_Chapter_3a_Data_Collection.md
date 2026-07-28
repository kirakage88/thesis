# Chapter III (Part 1): Data Collection

## 3.1 Data Collection

### 3.1.1 Research Design Overview

**Experimental Research Design** — the study implements a controlled, systematic, and instrumented data collection procedure using calibrated sensors, synchronized microcontroller nodes, and repeated measurement trials under uniform conditions.

Key characteristics:
- Standardized hardware setup across all 50 AC units.
- Sensor calibration experiments conducted prior to deployment.
- Strict measurement protocols for consistency and reproducibility.
- All sensors (BME280, DS18B20, ACS712, ZMPT101B, ESP32-CAM) collect data simultaneously via **ESP-NOW synchronized timestamp**.
- 6-month monitoring period observing naturally occurring behaviors (temperature variations, ice formation, noise, refrigerant conditions).
- Systematic repeated measurement enables correlation between operating conditions and early signs of abnormalities.

The study aims to compare ML models (CNN, RF, XGBoost, k-NN, RBF SVM, DNN) using controlled trial data.

### 3.1.2 Sources of Data

| Feature | Data Type | Sensor | Purpose |
|---------|-----------|--------|---------|
| Ambient Temperature | Continuous | BME280 | Environmental temp influencing AC load |
| Humidity | Continuous | BME280 | Moisture levels contributing to coil icing |
| Pressure | Continuous | BME280 | Atmospheric pressure for thermal profiling |
| Inlet Air Temp | Continuous | DS18B20 | Temperature entering indoor unit |
| Outlet Air Temp | Continuous | DS18B20 | Temperature leaving indoor unit — cooling performance |
| Coil Surface Temp | Continuous | DS18B20 | Abnormal coil temp indicating frost/fouling/refrigerant issues |
| Compressor Current Draw | Continuous | ACS712 | Electrical load — detects inefficiencies and early faults |
| Fan Motor Current | Continuous | ACS712 | Airflow anomalies and motor degradation |
| Supply Voltage | Continuous | ZMPT101B | Voltage fluctuations affecting performance |
| Frost Build-Up | Nominal | ESP32-CAM + CNN | Image-based classification of frost presence |
| Coil/Fin Condition | Nominal | ESP32-CAM + CNN | Cleanliness, fin blockage, fouling detection |

Total: **11 features** per unit (9 continuous, 2 nominal from image classification).

### 3.1.3 Sampling

**Purposive sampling** — units that best represent real-world academic environment usage.

- Maximum **50 split-type AC units** across 3 locations:
  1. **SBM-AVR** — high operational hours, tendency for dirt/humidity accumulation.
  2. **College of Engineering Building** — faculty rooms and labs, easy access for weekly measurement.
  3. **Faber Hall** (1st floor only) — completes sample size with consistent monitoring.

### 3.1.4 Hardware Used

Three node types, each with an ESP32-C3 microcontroller:

#### Ambient and Temperature Node
- ESP32-C3 (microcontroller)
- BME280 — ambient temp, humidity, pressure
- DS18B20 ×3 — inlet air temp, outlet air temp, coil surface temp

#### Electrical Node
- ESP32-C3 (microcontroller)
- ACS712 ×2 — compressor current draw, fan motor current
- ZMPT101B — supply voltage

#### Frost Node
- ESP32-CAM — coil/fin condition classification and frost build-up detection

**Communication:** All ESP32 nodes share data via **ESP-NOW**. One ESP32 serves as **Master** — collects all data + timestamps, then stores/sends to a PC/server. All nodes take measurements at the same timestamp.

### 3.1.5 Data Gathering Procedure

1. **Preparation & Scheduling:** ~50 units tested weekly over ~6 months.
2. **Data Gathering:** Each unit undergoes **10 measurement trials** per visit. Categorized as Normal/Abnormal based on expert-validated criteria.
3. **Data Labeling (2 steps):**
   - Step 1: Images classified per established criteria.
   - Step 2: Measurement data assigned final label by matching with image classification → Normal or Abnormal.

### 3.1.6 Validity and Reliability Measures

The study's predictive model depends on data quality — a robust validation phase is critical.

#### Sensor Validation Experiment Design

A **separate validation experiment** is conducted before the 6-month data gathering. The goal: quantify and correct manufacturing tolerances and measurement errors for each sensor.

**Scale:** 350 individual COTS sensors require validation (50 BME280, 150 DS18B20, 100 ACS712, 50 ZMPT101B). Individual calibration is logistically prohibitive, so **batch calibration** is used — multiple sensors of the same type tested simultaneously against a superior-grade reference instrument.

#### General Validation Procedure

1. **Unique Identification (UID):** Each sensor assigned a UID. DS18B20 uses its native 64-bit 1-Wire serial code. Others get human-readable labels (e.g., BME-01 to BME-50).
2. **Batch Testing:** Sensors tested in batches within a controlled environment.
3. **Reference Comparison:** Measurements correlated against a traceable, high-precision reference instrument.
4. **CCF Derivation:** A Calibration Correction Function (CCF) derived per UID — ranging from a simple offset to a non-linear polynomial.
5. **Database Storage:** All UIDs and CCF coefficients stored in a central calibration database (JSON/CSV) for automated preprocessing.

#### BME280 Validation (Temperature, Humidity, Pressure)

- **Reference:** Traceable thermo-hygrometer (e.g., Vaisala HMP 35A) for temp/humidity. METAR station data for pressure.
- **Environment:** Sealed environmental chamber with saturated salt solutions for known humidity levels. Peltier element for temperature control.

**Critical consideration:** The BME280 datasheet warns of self-heating — the internal temperature reading is above ambient. Since the Thermal Node PCB co-locates the BME280 with an ESP32-C3 (a heat source), validation must be performed on the **fully assembled Thermal Node** to characterize the systemic thermal offset.

**Temperature calibration:** 3 setpoints (15°C, 25°C, 35°C), 30-min stabilization, 10-min data logging. Linear regression per UID: `T_corrected = m × T_raw + c`.

**Humidity calibration:** 2-point using NaCl (~75% RH) and MgCl₂ (~33% RH). Linear regression per sensor.

**Pressure calibration:** 1-hour lab run, reference from METAR station, altitude-corrected via barometric formula.

#### DS18B20 Validation (Temperature)

- **Reference:** Fluke Hart Scientific standard sensor or ASTM 117C thermometer (0.01°C resolution).
- **Environment:** Temperature-controlled liquid bath with circulation pump (mandatory — eliminates thermal stratification).
- **Key advantage:** 1-Wire bus protocol allows all 150 sensors on a single bus; each uniquely identifiable by its 64-bit serial code. Enables automated mass calibration via a single microcontroller.

**Multi-point calibration:** Ice point (~0°C) using crushed ice + distilled water bath. Additional points via controlled bath. Master script polls all sensors every 10 seconds for 10 minutes.

#### ACS712 Validation (Current)

- **Reference:** True-RMS DMM (e.g., Fluke 115) — **non-negotiable** because compressor/fan motors are inductive loads producing non-sinusoidal waveforms.
- **Loads:** High-power resistive loads (50W, 200W, 250W).
- **Two error sources:**
  1. **Zero-current offset:** Quiescent voltage when no current flows — "fluctuates A LOT" and must be calibrated per sensor.
  2. **Sensitivity (gain):** Actual mV/A scaling factor with manufacturing tolerance.

**Procedure:** Node powered on with no AC load. 1000 ADC readings over 60 seconds averaged to determine `ADC_Zero_Offset` per sensor. Stored in calibration database.

#### ZMPT101B Validation (Voltage)

- **Reference:** True-RMS DMM (e.g., Fluke 115).
- **Source:** Variable AC Transformer (Variac) for adjustable voltage across 50–250V range.

**Key finding from literature:** The ZMPT101B output is **not truly linear**. A **3rd-order polynomial regression** gives the best relationship. A simple linear calibration is scientifically insufficient.

**Standardization step:** Adjust onboard trimpot so max expected voltage (250V) maps to an ADC value below saturation (~640), providing headroom.

### 3.1.7 Data Management and Storage

Comprehensive Data Management Plan (DMP) for the 6-month monitoring period, adhering to **FAIR principles** (Findable, Accessible, Interoperable, Reusable).

#### Storage Architecture

- **On-Site Ingest:** Master ESP32 transmits synchronized data payload + timestamp to a central Ingest Server (dedicated PC) via private Wi-Fi.
- **Primary Storage (NAS):** Ingest Server writes data to a Network Attached Storage device — the primary high-availability repository.
- **Off-Site Cloud:** NAS performs automated nightly sync to secure academic cloud storage (AWS S3, Google Cloud, or university repository).

#### Logical Directory Structure

"Advanced Project" folder structure separating data by processing stage:

```
Project_Root/
├── 01_Sensor_Calibration/    # CCF database
├── 02_Data/
│   ├── raw/                   # Immutable original data
│   ├── interim/               # Cleaned + CCF-applied data
│   └── processed/             # Feature-engineered datasets for ML
├── 03_Code/
│   ├── 1_ingest/
│   ├── 2_preprocessing/
│   └── 3_modeling/
└── 04_Outputs/
    └── models/                # Trained model files (.pkl, .pth)
```

#### File Naming Convention

`YYYYMMDDTHHmmSSZ_<Location>_<UnitID>_<TrialNum>_<DataType>.csv`

Example: `20251116T110400Z_SBM-AVR_ACU-01_T03_RAW.csv`

Data types: `RAW` (sensor data CSV), `IMG` (ESP32-CAM image), `LOG` (system health logs).

#### Data Protection: The 3-2-1 Backup Rule

- **3 copies** of the data.
- On **2 different media types**.
- **1 copy off-site**.

Implementation:
1. **Copy 1:** Primary on-site NAS (hot data for daily access).
2. **Copy 2:** External USB HDD connected to NAS (different media, weekly full backup).
3. **Copy 3:** Encrypted nightly cloud sync (geographic redundancy).

Recovery protocol tested quarterly by restoring random data subsets from cloud backup.

#### "Keep Raw Data Raw" Policy

Raw data files in `02_Data/raw/` are **sacrosanct** — never altered.

Implementation:
- Files set to **read-only** after successful write.
- **No manual edits** — spreadsheet software explicitly forbidden.
- All preprocessing performed exclusively via **documented scripts** (Python/Pandas, R).
- Scripts **read from raw/**, transform in memory, **write new files to interim/**.

This ensures **100% reproducibility**: any researcher can re-run the scripts on raw data and regenerate all outputs.
