# Chapter I: Introduction

## 1.1 Background of the Study

> **STAGED DRAFT — JRP's edits only. Compare against `documents/01_Chapter_1_Introduction.md`.**
>
> **Title alternatives (JRP task, needs adviser re-approval):**
>
> **Option A (primary):** DEVELOPMENT OF A PREDICTIVE MAINTENANCE FRAMEWORK USING NON-INVASIVE ANOMALY DETECTION FOR COILED EVAPORATORS IN SPLIT-TYPE AIR CONDITIONING SYSTEMS AT XAVIER UNIVERSITY – ATENEO DE CAGAYAN
>
> **Option B:** DEVELOPMENT OF A PREDICTIVE MAINTENANCE FRAMEWORK VIA NON-INVASIVE ANOMALY DETECTION FOR COILED EVAPORATORS IN SPLIT-TYPE AIR CONDITIONING SYSTEMS AT XAVIER UNIVERSITY – ATENEO DE CAGAYAN
>
> **Option C:** DEVELOPMENT OF A NON-INVASIVE ANOMALY DETECTION SYSTEM FOR PREDICTIVE MAINTENANCE OF COILED EVAPORATORS IN SPLIT-TYPE AIR CONDITIONING SYSTEMS AT XAVIER UNIVERSITY – ATENEO DE CAGAYAN
>
> **Approved (original):** DEVELOPMENT OF A PREDICTIVE MAINTENANCE MODEL FOR COILED EVAPORATORS IN SPLIT-TYPE AIR CONDITIONING SYSTEMS INSTALLED IN THE COLLEGE OF ENGINEERING BUILDING, FABER HALL, AND SBM AVR AT XAVIER UNIVERSITY – ATENEO DE CAGAYAN
>
> Changes: "Model" → "Framework" (matches 4-model architecture + conditional secondary); added "Non-Invasive Anomaly Detection" qualifier to signal actual methodology; removed specific building names from title (locations specified in 1.5 scope instead). ⚠️ Requires adviser re-approval — title deviates from the approved proposal.

---

Air conditioning is essential for thermal comfort in hot/humid climates like the Philippines, but accounts for a large share of building energy consumption. Split-type ACs are widely used for their efficiency and compact design. The evaporator coil is critical — its condition directly affects cooling performance, energy use, and system lifespan.

Evaporator coils degrade from dust, corrosion, microbial growth, refrigerant issues, and poor maintenance. A study by Niknami et al. (2024) shows that fouling just **30% of an evaporator surface** causes a **13.5% drop in EER**, a **6.4% increase in energy consumption**, and a **19.1% reduction in cooling load**.

<!-- JRP EDIT: Research gap rewritten (roadmap line 47) -->
Scheduled preventive maintenance ensures regular cleaning every 3–4 months, but the interval between services creates an information gap: maintenance staff cannot reliably identify which specific units are experiencing early-stage performance degradation between visits without physical disassembly. This study investigates whether a non-invasive sensor system — using only external temperature, electrical, and vibration measurements, with no evaporator access — can detect anomalous operating behavior, serving as a complementary triage tool to existing preventive maintenance at Xavier University. As Xavier University develops its Campus of the Future, this study serves as a proof-of-concept for site-specific, non-invasive AC condition monitoring.

<!-- TODO(SFS): SFS owns "Strengthen RA 11285 rationale" (roadmap line 94): add quantified energy savings estimate (~₱115,000 annual waste). -->
This study aligns with **RA 11285** (Energy Efficiency and Conservation Act), which mandates energy-efficient technologies in both public and private sectors.

<!-- TODO(CBA): The next paragraph (PdM framing) — CBA owns "Reframe positioning as complementary triage" (roadmap line 86). The text below is the original generic PdM intro; CBA should rewrite it to emphasize that this system is a diagnostic layer that flags which units need attention between cleanings, does NOT replace scheduled preventive maintenance. -->
Predictive Maintenance (PdM), powered by AI/ML and IoT, provides a proactive solution by analyzing real-time sensor data to anticipate failures before they occur.

### Research Questions

<!-- JRP EDIT: Old RQs replaced with roadmap lines 70-73 -->

1. **RQ1:** Which non-invasive sensor measurements (supply-return temperature differential, compressor/fan current signatures, vibration spectral features) demonstrate the strongest discriminatory power for distinguishing normal from degraded unit behavior, as measured by feature importance and anomaly score separation?

2. **RQ2:** Which unsupervised anomaly detection model (Autoencoder, Isolation Forest, One-Class SVM, Gaussian Mixture Model) most reliably identifies AC units exhibiting anomalous operating signatures, validated through retrospective log comparison and controlled fault injection?

3. **RQ3 (conditional):** Does replacing raw environmental sensor features with a composite thermal comfort metric (PMV) improve anomaly detection sensitivity, provided the DIY airflow sensor is successfully developed?

4. **RQ4:** Does anomaly score generalize across AC units not seen during model development (unit-level evaluation), and does time-since-last-cleaning confound anomaly detection?

### Hypotheses

<!-- JRP EDIT: New subsection added (roadmap lines 79-82) -->

- **H1:** At least one unsupervised model achieves anomaly score separation between known-fault and known-healthy units with p < 0.05 (Mann-Whitney U test) and true positive rate ≥ 80% on injected faults.

- **H2:** PCA-reduced features achieve anomaly detection performance within 3 percentage points of the full feature set AND show no statistically significant difference in unit-level anomaly ranking (p > 0.05, McNemar's test).

- **H3:** Vibration-derived features (spectrogram CNN output or statistical features) contribute statistically significant improvement to anomaly detection over sensor-only features (p < 0.05, paired bootstrap).

- **H4 (conditional):** Replacing raw environmental features with PMV does not significantly degrade anomaly detection performance (within 3pp of raw-feature baseline) — demonstrating that an ME-derived composite metric is a viable alternative.

---

<!-- ========== SECTIONS BELOW: NOT YET REWRITTEN (other owners) ========== -->

## 1.2 Main Objective

<!-- TODO(CBA): This section references supervised classifiers (Hybrid RF+CNN, XGBoost, k-NN, DNN) which conflict with the unsupervised anomaly detection pivot.
     CBA owns "Justify unsupervised over supervised" (roadmap line 108) and "Add unsupervised methodology justification — 3.3" (roadmap line 148).
     The objective should be rewritten to reflect: unsupervised anomaly detection as primary approach, supervised as conditional secondary.
     Current text preserved verbatim below for diff review. -->

Design and develop a predictive maintenance model for coiled evaporators in split-type AC systems using AI techniques. Analyze critical operational parameters (air temperature, ice build-up, compressor current, supply voltage) to classify system condition as **normal** or **abnormal** and optimize maintenance schedules.

## 1.3 Specific Objectives

<!-- TODO(CBA): Same issue as 1.2 — lists obsolete supervised models (Hybrid RF+CNN, XGBoost, k-NN, RBF SVM, DNN).
     CBA to rewrite per roadmap: ensure objectives reflect unsupervised anomaly detection (Autoencoder, Isolation Forest, One-Class SVM, GMM)
     with conditional secondary (RF, XGBoost, RBF SVM if ≥30 labeled samples). Current text preserved verbatim below. -->

1. Establish a data acquisition and preprocessing pipeline with statistical feature selection/extraction to ensure input data quality and relevance.
2. Select and validate the top-performing predictive model by comparing: **Hybrid RF+CNN, XGBoost, k-NN, RBF SVM, DNN** using precision, sensitivity, and F1 scores.
3. Propose a Maintenance 4.0 framework using cloud-based or self-hosted workflow integrating real-time data collection, model analysis, and system monitoring.

## 1.4 Conceptual Framework

<!-- TODO(SFS): SFS owns "Fix variable-sensor mapping — 1.4" (roadmap line 51).
     Remove: refrigerant leaks (no gas sensor), ice build-up (non-invasive constraint), ESP32-CAM.
     Rename: "noise" → "vibration" (MPU6050).
     Add: set temperature (manually recorded from thermostat/remote).
     Create explicit mapping table: Independent Variable → Sensor → Data Type → Model Input.
     Redraw conceptual framework diagram.
     Current text preserved verbatim below. -->

- **Independent variables:** Air temperature, noise, ice build-up, refrigerant leaks — operational indicators of system health.
- **Mediating variable:** The ML model (AI techniques + IoT data acquisition) — transforms raw sensor data into actionable insights.
- **Dependent variable:** Predictive maintenance outcome — the model's ability to accurately forecast failures and support proactive maintenance.

The framework emphasizes that the AI model is the mechanism that translates raw sensor readings into maintenance decisions.

## 1.5 Limitations

<!-- TODO(SFS): SFS owns "Update scope and limitations for non-invasive approach — 1.5" (roadmap line 100).
     Rewrite to reflect: non-invasive external sensors only; 30-40 units across 3 locations; weekly visits with 2 portable kits;
     anomaly detection as triage tool; long-term Campus of the Future vision.
     Acknowledge: cannot directly observe evaporator; model detects proxy signals; weekly sampling misses transients;
     portable kit mounting variability (mitigated by protocol + kit ID); fault injection is experimental design, not deployment.
     Also add scope diagram (roadmap line 116).
     Current text preserved verbatim below. -->

1. **Time-constrained data collection:** Natural coil fouling takes weeks/months. The study uses cloth/mesh to simulate fouling in a short timeframe, which doesn't perfectly replicate real dust accumulation or corrosion.
2. **Budget sensor accuracy:** Low-cost sensors with ±2–5% error margins introduce noise into the dataset, increasing false alarm/missed fault risk.
3. **Setup cost and integration challenges:** Multiple sensor installation and coordination is technically and financially demanding. Limited infrastructure constrains integration complexity.
4. **Modeling complexity vs. student expertise:** Models are limited to binary classification (normal/abnormal). Regression-based approaches require more advanced skills and higher-precision sensors.

Despite these limitations, the study provides a viable foundation for PdM in coiled evaporators using readily available resources.

## 1.6 Definition of Terms

<!-- TODO(SFS): Terms "Ice Build-Up", "Refrigerant Leak", "Noise (acoustic)" need removal or replacement
     as part of SFS's 1.4 variable-sensor mapping fix. Current text preserved verbatim below. -->

Key terms defined include: Anomaly Detection, Artificial Intelligence, Coiled Evaporator, CNN, Dataset, Feature Extraction, Heat Map, Ice Build-Up, IoT, Machine Learning, Model Accuracy, Neural Network, Noise (acoustic), Overfitting, Predictive Maintenance, Random Forest, Refrigerant Leak, Sensor Data, Split-Type AC System, Temperature, and Validation.

---

## TODO (other owners)

Summary of Chapter 1 tasks **not yet completed** — belonging to SFS and CBA. Each task references the exact roadmap line for details.

### Simon Sulibio (SFS)

| Roadmap line | Section | Task |
|--------------|---------|------|
| 51 | 1.4 | Fix variable-sensor mapping: remove refrigerant leaks, ice build-up, ESP32-CAM; rename "noise" → "vibration"; add set temperature; create mapping table; redraw diagram |
| 94 | 1.1 | Strengthen RA 11285 rationale: add quantified energy savings (~₱115,000 annual waste) |
| 100 | 1.5 | Update scope and limitations for non-invasive approach (see roadmap for full text) |
| 116 | 1.5 | Add scope diagram (in scope vs. out of scope, non-invasive focus) |
| — | 1.6 | Remove/replace "Ice Build-Up", "Refrigerant Leak", "Noise (acoustic)" from Definition of Terms |

### Collin Brandon Asio (CBA)

| Roadmap line | Section | Task |
|--------------|---------|------|
| 61 | 1.1 / 3.1 | Add operational definition of Normal/Degraded |
| 86 | 1.1 | Reframe positioning as complementary triage: explicitly state system does NOT replace scheduled PM; reference maintenance logs as evidence |
| 108 | 1.5 or 3.3 | Justify unsupervised over supervised: walk through 13-in-2,599 data constraint |
| — | 1.2, 1.3 | Rewrite Main/Specific Objectives to reflect unsupervised primary + supervised conditional secondary |
