# Chapter I: Introduction — Suggestions & Loopholes

## Loopholes

### L1. Mismatch Between Conceptual Framework Variables and Actual Hardware

The conceptual framework (1.4) lists **independent variables** as: air temperature, noise, ice build-up, and refrigerant leaks. However, the hardware design (3.1.4) includes:
- BME280 (temp, humidity, pressure)
- DS18B20 (3× temp probes)
- ACS712 (compressor & fan current)
- ZMPT101B (supply voltage)
- ESP32-CAM (frost, coil condition)

**Missing sensors:**
- **No acoustic/noise sensor** — "noise" is listed as an independent variable but no microphone or sound sensor is in the hardware design.
- **No refrigerant leak sensor** — "refrigerant leaks" is listed but no gas/leak detector is specified.

Either remove these from the conceptual framework or add the corresponding sensors.

### L2. Scope Feasibility for a Bachelor's Thesis

- **50 AC units** × **7 sensors each** = **350 sensors** to calibrate and deploy.
- **6-month monitoring period** with weekly visits to 3 locations.
- **10 trials per unit per visit** = 500 trials per week.
- Simultaneously developing 6 ML models, a Streamlit dashboard, ESP32-CAM CNN, and ESP-NOW networking.

This is ambitious for a 3-person bachelor's thesis. Consider reducing the scope (fewer units, shorter monitoring, fewer models) or clarifying how this is achievable with available resources.

### L3. Vague Research Question 3

> "How can the proposed framework be designed to successfully integrate real-time data collection and model analysis into a cloud-based or self-hosted proactive maintenance workflow?"

This is more of an engineering task than a research question. It doesn't ask a testable hypothesis. Consider reframing to ask about the comparative performance of cloud-based vs. self-hosted deployment, or about the latency/accuracy tradeoffs.

### L4. Fouling Simulation Validity

Section 1.5 acknowledges that cloth/mesh is used to simulate fouling, which "fails to accurately mimic the natural accumulation of dust, microbial growth, or corrosion." This is a major external validity threat that could undermine the entire model's real-world applicability. Consider:
- Adding a small set of naturally fouled coils for comparison.
- Discussing transfer learning as a mitigation strategy.

## Suggestions for Improvement

### S1. Tighten the Variable-Sensor Mapping
Create an explicit table in the conceptual framework section mapping each independent variable to its corresponding sensor and data type. This prevents the mismatch identified in L1.

### S2. Strengthen RA 11285 Connection
The RA 11285 alignment is mentioned once and not revisited. Add a specific paragraph quantifying potential energy savings (e.g., "if deployed across Xavier University's N AC units, the model could save X kWh/year based on the 6.4% energy increase from fouling").

### S3. Add a Clear Hypothesis
The research questions are descriptive. Add formal testable hypotheses, e.g.:
- H1: "At least one of the tested ML models achieves statistically significantly higher F1 score than 0.85 for binary classification of evaporator coil condition."
- H2: "PCA-reduced features achieve comparable or better model performance than the full 11-feature dataset."

### S4. Justify Binary Classification Choice
The limitations section mentions regression was rejected due to complexity and sensor accuracy. Strengthen this justification with a brief argument that binary classification (normal/abnormal) is the industry standard for initial PdM deployment and is more actionable for maintenance personnel than a continuous degradation score.

### S5. Clarify "Expert-Validated" Labeling Criteria
Section 3.1.5 states units are categorized as Normal/Abnormal "based on criteria validated by experts." Who are these experts? What are the specific criteria? Without this, the ground truth labels are unvetted. Define the criteria explicitly (e.g., "Abnormal = visible frost covering >20% of coil surface, OR inlet-outlet temp differential < 3°C, OR compressor current > X A").