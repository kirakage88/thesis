# Chapter III (Part 1): Data Collection — Suggestions & Loopholes

## Loopholes

### L1. ESP32-C3 ADC Limitations for ACS712

The ACS712 is an **analog** Hall-effect sensor read via the ESP32-C3's ADC. The ESP32-C3 ADC is known for:
- **Non-linear response** at the low and high ends of the range.
- **12-bit resolution** (0–4095) over 0–3.3V — coarse for small current measurements.
- **High noise** — the ESP32 ADC has a reported ENOB (effective number of bits) of ~9–10 bits, not the full 12.

For the Fan Motor Current (expected 0–1A range), this is critical. The ACS712's already-noisy output at low currents, combined with the ESP32's noisy ADC, may produce unusable data. The methodology doesn't address this beyond "average 1000 readings."

**Suggestion:** Consider an external ADC (e.g., ADS1115, 16-bit) for the ACS712 readings, or switch to a digital current sensor (e.g., INA219 for low-side current sensing).

### L2. ESP32-CAM Image Transmission via ESP-NOW

The Frost Node uses ESP32-CAM for image capture, but ESP-NOW has a **maximum payload of 250 bytes** per packet. A single QVGA (320×240) JPEG is typically 10–50 KB — far exceeding ESP-NOW's limit.

The methodology says "All ESP32 shares data through ESP Now Communication where one ESP32 serves as the Master" but doesn't explain how images are transmitted:
- Are images chunked and reassembled?
- Is Wi-Fi (TCP/HTTP) used for images instead of ESP-NOW?
- Are images processed on-device (CNN on ESP32-CAM via TinyML/Edge Impulse) and only the classification result transmitted?

**This is a critical architectural gap.** Clarify the image data path.

### L3. No Power Management Discussion

The sensor nodes (especially the Frost Node with ESP32-CAM) will draw significant current. The methodology doesn't discuss:
- How are the nodes powered? (USB, battery, AC unit's own power?)
- Battery life expectations if battery-powered.
- Sleep/wake cycles for power optimization.
- Whether nodes are permanently installed or temporary (brought for weekly visits).

If nodes are brought for weekly visits (10 trials), this should be stated clearly — it changes the "6-month continuous monitoring" claim.

### L4. Ambiguity: Continuous Monitoring vs. Weekly Visits

Section 3.1.1 states "6-month monitoring period" with "controlled trials per scheduled visit" and "10 measurement trials." Section 3.1.3 mentions "uniform weekly measurement." But the DMP (3.1.7) describes real-time, near-continuous data ingestion from Master ESP32 nodes.

**Clarify:** Is this continuous 6-month monitoring (sensors installed and left) or periodic weekly visits (sensors brought, 10 trials conducted, sensors removed)? These are fundamentally different experimental designs with different data characteristics.

### L5. Batch Calibration Feasibility

The validation plan assumes access to:
- A sealed environmental chamber with Peltier temperature control.
- Saturated salt solutions for humidity calibration (NaCl, MgCl₂).
- A liquid circulation bath with pump.
- A Fluke Hart Scientific reference thermometer ($1000+).
- A True-RMS DMM (Fluke 115, $200+).
- A Variac ($100+).

For a bachelor's thesis with budget constraints (acknowledged in 1.5), access to all this equipment is uncertain. The plan should note which equipment is confirmed available at Xavier University's labs and which needs to be sourced externally.

### L6. No Sampling Frequency Specification

The methodology doesn't specify:
- How often sensors take readings (1 Hz? 1 reading/second? 1 reading/minute?).
- Duration of each "trial" (10 trials per visit — but how long is one trial?).
- Whether readings are instantaneous or averaged over a time window.

Without sampling frequency, the expected dataset size and temporal resolution are unknown.

### L7. ZMPT101B 3rd-Order Polynomial — No Implementation Detail

Section 3.1.6 correctly identifies that a linear model is insufficient for ZMPT101B and recommends a 3rd-order polynomial. However:
- No actual polynomial form is given.
- No reference to the specific peer-reviewed study that established this.
- No explanation of how the polynomial coefficients will be stored and applied in real-time on the ESP32.

### L8. No Sensor Failure / Missing Data Protocol

The DMP addresses backup and redundancy for storage, but not for **sensor failure during deployment**:
- What happens if a DS18B20 probe disconnects?
- What happens if the ESP32-CAM loses focus or captures a blurry image?
- How are malformed/missing readings handled in real-time before the automated inference pipeline touches them?

## Suggestions for Improvement

### S1. Add a System Architecture Diagram
Include a clear block diagram showing:
- All 3 node types with their sensors.
- ESP-NOW vs. Wi-Fi data paths (clarifying image transmission).
- Data flow from nodes → Master → Ingest Server → NAS → Cloud.
- Power source for each node.

### S2. Clarify the Monitoring Regime
Explicitly state whether the system is:
- **Option A:** Continuous 6-month installation (sensors permanently mounted, powered by AC unit).
- **Option B:** Weekly visit protocol (portable sensor kit, 10 trials, then removed).

This fundamentally affects the data's temporal characteristics and the ML model's applicability.

### S3. Add Sampling Parameters Table
Include a table specifying for each sensor:
- Sampling rate (Hz or samples/second).
- Trial duration (minutes).
- Number of readings per trial.
- Total expected data volume per unit per visit.

### S4. Address the Image Transmission Architecture
If ESP-NOW can't handle images, specify the alternative:
- Process on-device with TinyML and send only the classification label via ESP-NOW.
- Use Wi-Fi (HTTP/MQTT) for image upload.
- Store images on SD card and transfer manually.

The on-device TinyML approach is the most elegant and aligns with the literature on edge computing. Consider training a quantized CNN that runs directly on the ESP32-CAM.

### S5. Include an Equipment Availability Matrix
A table listing each piece of calibration equipment, whether it's available at XU labs, and a fallback plan if not available. This demonstrates feasibility awareness.

### S6. Define Expert-Validated Labeling Criteria
Provide the exact criteria for "Normal" and "Abnormal" classification, agreed upon with HVAC technicians or the research adviser. This ensures label consistency across the 6-month study.