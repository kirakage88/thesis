# Chapter II: Literature Review — Suggestions & Loopholes

## Loopholes

### L1. Descriptive Rather Than Critical Synthesis

Each of the 10 studies is summarized descriptively — what the study did and found. There is minimal **critical analysis** of:
- Methodological weaknesses in cited studies.
- Contradictions between studies (e.g., one study found RF best, another found DT best — why?).
- Transferability of findings to this thesis's specific context (tropical climate, split-type residential AC, low-cost sensors).

A literature review should synthesize and critically evaluate, not just summarize.

### L2. No Explicit Research Gap Identification

The chapter reviews 10 papers but never explicitly states: "Based on these studies, the following gaps remain..." The gaps are implied but not articulated. This weakens the justification for the study.

### L3. Tangentially Related Studies

- **2.8 (Aji et al., 2020)** — magnetic sensor PdM for geophysical networks. This has no direct connection to HVAC or air conditioning. It only demonstrates that RF works well — which is already established by HVAC-specific studies.
- **2.9 (Abood et al., 2023)** — electromechanical motor PdM using GAN+CNN. Again, not HVAC-specific.

Consider replacing these with more directly relevant HVAC/commercial AC PdM studies.

### L4. No Discussion of Datasets and Data Availability

None of the reviews mention:
- What datasets were used (public vs. private, sample sizes, class balance).
- Whether the data is reproducible or available.
- Data collection duration and sampling frequency.

This matters because this thesis will face significant data collection challenges (6 months, 50 units). Understanding how others handled data scarcity would be valuable.

### L5. Missing Recent Literature on Key Technologies

- No mention of **ESP-NOW** or low-power wireless protocols for IoT sensor networks.
- No discussion of **edge computing / TinyML** — running ML models directly on ESP32 for real-time inference.
- No literature on **ESP32-CAM** for industrial inspection or HVAC monitoring.

### L6. No Framework Comparison

Multiple frameworks are mentioned (autoencoders, CNN-GAN, MPC+ML, DPCA+VGG) but there is no comparative analysis of which framework best fits this thesis's constraints (low-cost, low-power, limited compute).

## Suggestions for Improvement

### S1. Add a Synthesis Section
After the 10 individual reviews, add a dedicated "Synthesis and Research Gap Analysis" section that:
- Compares the studies in a multi-dimensional table (model, dataset size, accuracy, HVAC type, sensor type, deployment context).
- Explicitly lists 3–5 research gaps this thesis addresses.
- Justifies the choice of models (RF, SVM, XGBoost, k-NN, DNN, Hybrid CNN+RF) over alternatives based on the literature.

### S2. Replace Tangential Studies
Replace 2.8 (magnetic sensors) and 2.9 (electromechanical motors) with:
- A study on **ESP32-based IoT sensor networks** for building monitoring.
- A study on **low-cost sensor calibration** for predictive maintenance.
- A study specifically on **evaporator coil fouling** detection (Niknami et al., 2024 is cited in the intro but not reviewed in the RRL).

### S3. Add a Conceptual Framework Diagram
The synthesis section should include a conceptual model showing how the literature informs this thesis's architecture: sensor selection → preprocessing → model choice → deployment strategy.

### S4. Discuss Data Imbalance Challenge
Several reviewed studies use classification (normal/abnormal). In real HVAC systems, abnormal conditions are rare. Add a paragraph discussing how the literature handles **class imbalance** (SMOTE, cost-sensitive learning, anomaly detection) and how this thesis will address it.

### S5. Add Citation for Foundational ML Concepts
Section 2.10 (Sarker, 2021) is used as the sole reference for KNN, SVM, DT, RF, XGBoost, and CNN basics. While comprehensive, consider citing the original/benchmark papers for each algorithm (e.g., Breiman 2001 for RF, Chen & Guestrin 2016 for XGBoost, Cortes & Vapnik 1995 for SVM) to strengthen academic rigor.