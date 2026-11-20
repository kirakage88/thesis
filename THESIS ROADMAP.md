# nThesis Roadmap — Predictive Maintenance for Coiled Evaporators

Group: John Ronald Pacaldo · Collin Brandon Asio · Simon France Sulibio

**Architecture Decision:** Unsupervised anomaly detection (primary) \+ supervised classification (secondary, conditional). \[See appendix for full A vs B analysis.\]  

[Thesis Proposal](https://myxueduph-my.sharepoint.com/:w:/r/personal/200931726_my_xu_edu_ph/_layouts/15/Doc.aspx?sourcedoc=%7B891c7bba-5c73-4f82-9bec-46f610221ec8%7D&action=edit&wdPreviousSession=758f6eb9-f42f-9fa8-8383-e8d3636bb8bd) 

[Original Thesis Proposal](https://myxueduph-my.sharepoint.com/:w:/g/personal/200931726_my_xu_edu_ph/Ee4_vBncjnRJt547xa2E6jIBxna6wo3hHIDagz53lBNfjw?e=SMliZX&fbclid=IwY2xjawUghc5wZG9mAWV4dG4DYWVtAjEwAGJyaWQRMVRiOXNSMkh6NjJ1NkE4a21zcnRjBmFwcF9pZBAyMjIwMzkxNzg4MjAwODkyAAEeR82DdXaALuucZvr_mFMndykw-cS43Epp2AeLiQrdk79Sm9wgM74oYsDLgd4_aem_RauMoN4_f0lA2Txq0kAsbA)

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

## How to Read This Roadmap

This document tracks a group thesis with two kinds of work running in parallel: **writing the paper** (📝/📋 tasks — Chapters 1–5) and **building the actual system** (🔧/💻/🤖/📊/🚀 tasks — hardware, code, data, models, dashboard). The phases are ordered so paper tasks lock down decisions *before* the matching build work starts, and later chapters get rewritten once the build produces real results.

**The 10 phases at a glance:**

1. Lock the research direction on paper before touching hardware  
2. Build and test the two portable sensor kits  
3. Rewrite the literature review to match the new direction  
4. Calibrate the two sensors that need lab equipment  
5. Write up the model designs in detail  
6. Run the actual 6-month data collection  
7. Train the vibration model  
8. Train and validate the main anomaly-detection models  
9. Build the live dashboard  
10. Pull everything together into the final document and defense

**Recurring terms, in plain language:**

| Term | What it means here |
| :---- | :---- |
| Unsupervised anomaly detection | The model learns what "normal" AC behavior looks like from data with no fault labels, then flags anything that doesn't match — it never needs to be shown an example of a fault first |
| Supervised classification | The model instead learns from readings explicitly labeled "normal" or "faulty" — it needs a decent number of labeled faulty examples to work, which this study doesn't have much of |
| ESP-NOW | A lightweight wireless protocol that lets the ESP32 sensor boards send readings to a receiver without a full Wi-Fi network connection |
| CCF | "Calibration Correction Factor" — the formula (from Phase 4\) that turns a raw sensor reading into a real-world value, e.g. raw ADC number → actual amps |
| PPO | Xavier University's Physical Plant Office — the maintenance staff who currently clean and service the AC units |
| Reconstruction error | How different a model's "guess" at a normal reading is from the actual reading — the bigger the gap, the more anomalous |
| p \< 0.05 / p \> 0.05 | The threshold used to decide if a result is a real pattern (p \< 0.05) or could just be noise (p \> 0.05) — which one you want depends on what the hypothesis is claiming |
| TPR / FPR | True Positive Rate (% of real faults correctly flagged) / False Positive Rate (% of healthy units wrongly flagged) |
| LOUO | "Leave-One-Unit-Out" — testing the model on an AC unit it has never seen during training, to check it generalizes rather than memorizing specific units |

Each phase below now opens with a **Goal**, followed by an **In plain terms** line, before the checklist.

---

## **Phase 1 — Paper Overhaul: Foundation DONE**

**Goal:** Rewrite Chapter 1 and pre-prototyping sections of Chapter 3 to reflect the reframed thesis: non-invasive anomaly detection as a complementary triage tool for scheduled preventive maintenance. Lock down the architecture before any hardware work.

**In plain terms:** Before anyone touches a soldering iron, the paper has to say exactly what the thesis claims and how it'll be proven — otherwise Phase 2's hardware choices might not match the study design. This phase locks the story: what "normal" vs. "degraded" means, what questions the thesis answers, and what would have to be true for each answer to count as supported.

### Chapter 1 — Introduction

- [x] 🔴 **Rewrite the thesis title** — `1.1 JOHN PACALDO`  
  *→ The old title likely still implied the earlier, dropped approach — this makes sure the very first thing a reader sees matches the actual non-invasive, unsupervised study.*  
     
     
- [x] 🔴 **Rewrite the research gap** — `1.1 JOHN PACALDO`  
  *→ This is the paragraph that argues why the thesis needs to exist — it has to describe the real problem (the blind spot between scheduled cleanings) instead of the old framing, since everything else in Chapter 1 builds on this claim.*  
     
     
  \- \*\*Old:\*\* "No localized data-driven early warning exists; current maintenance is insufficient."    
     
  \- \*\*New:\*\* "Scheduled preventive maintenance ensures regular cleaning every 3–4 months, but the interval between services creates an information gap: maintenance staff cannot reliably identify which specific units are experiencing early-stage performance degradation between visits without physical disassembly. This study investigates whether a non-invasive sensor system — using only external temperature, electrical, and vibration measurements, with no evaporator access — can detect anomalous operating behavior, serving as a complementary triage tool to existing preventive maintenance at Xavier University. As Xavier University develops its Campus of the Future, this study serves as a proof-of-concept for site-specific, non-invasive AC condition monitoring."  
     
- [x] 🔴 **Fix variable-sensor mapping** — `1.4 Conceptual Framework SIMON SULIBIO`  
  *→ The original framework listed things the sensors can't actually detect (refrigerant leaks need a gas sensor, ice build-up needs evaporator access) — this strips those out and maps only what the real non-invasive hardware can measure.*  
     
     
  \- Remove: refrigerant leaks (no gas sensor), ice build-up (non-invasive access constraint), ESP32-CAM (cannot open evaporator)    
     
  \- Rename: "noise" → "vibration" (MPU6050 accelerometer)    
     
  \- Add: set temperature (manually recorded from thermostat/remote during each visit) — provides baseline for comparing actual vs. target cooling performance    
     
  \- Create explicit mapping table: Independent Variable → Sensor → Data Type → Model Input    
     
  \- Redraw conceptual framework diagram to match actual hardware and non-invasive approach  
     
- [x] 🔴 **Add operational definition of Normal/Abnormal** — `1.1 / 3.1 COLLIN ASIO`  
  *→ Without a written, agreed definition of "Normal" vs. "Degraded," there's no consistent way to label the 13 known-fault units used in later validation, or to judge results at all — this makes that call explicit.*  
     
     
  \- A unit is \*\*Normal\*\* if it exhibits acceptable cooling performance, no abnormal vibration or electrical behavior during inspection, and no maintenance concern is documented in the PPO maintenance logs.    
     
  \- A unit is \*\*Degraded\*\* if technician inspection identifies performance degradation, abnormal electrical or vibration characteristics, or a maintenance record documents a fault requiring corrective action.  
     
- [x] 🔴 **Rewrite research questions for unsupervised focus** *`JOHN PACALDO`*  
  *→ The RQs are the specific questions the whole thesis has to answer by the end — rewriting them for the unsupervised approach keeps every later phase working toward something concrete.*  
     
     
  \- \*\*RQ1:\*\* Which non-invasive sensor measurements (ambient, current and voltage signatures, vibration spectral features, and airflow) demonstrate the strongest discriminatory power for distinguishing normal from degraded unit behavior, as measured by feature importance and anomaly score separation?    
     
  \- \*\*RQ2:\*\* Which unsupervised anomaly detection model (Autoencoder, Isolation Forest, One-Class SVM, Gaussian Mixture Model) most reliably identifies AC units exhibiting anomalous operating signatures, validated through retrospective log comparison and controlled fault injection?    
     
  \- \*\*RQ3 (conditional):\*\* Does replacing raw environmental sensor features with a composite thermal comfort metric (PMV) improve anomaly detection sensitivity, provided the DIY airflow sensor is successfully developed?    
     
  \- \*\*RQ4:\*\* Does anomaly score generalize across AC units not seen during model development (unit-level evaluation), and does time-since-last-cleaning confound anomaly detection?  
     
- [x] 🔴 **Rewrite hypotheses (falsifiable with margins and tests)** *`JOHN PACALDO`*  
  *→ Each RQ needs a hypothesis that's falsifiable — a specific, testable claim with a stated pass/fail threshold and statistical test — otherwise "did the thesis succeed" has no objective answer at the end.*  
     
     
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
     
  \*\*Plain-English translation of H1a–H4b:\*\*  
     
    \- \*\*H1a:\*\* At least one type of sensor reading (temperature, current, or vibration) looks noticeably different on units known to have problems vs. healthy ones.  
     
    \- \*\*H1b:\*\* Adding the vibration sensor actually helps detect anomalies, beyond what temperature and electrical readings alone can catch.  
     
    \- \*\*H2a:\*\* At least one of the four models can both tell healthy and faulty units apart, and catch real injected faults at least 80% of the time.  
     
    \- \*\*H2b:\*\* Compressing the features with PCA doesn't meaningfully hurt performance — so a simpler feature set is a viable option.  
     
    \- \*\*H3 (conditional):\*\* If the DIY airflow sensor works, swapping in a single PMV comfort score instead of raw temperature/humidity/airflow doesn't meaningfully hurt performance either.  
     
    \- \*\*H4a:\*\* The model still works reasonably well on an AC unit it has never seen data from before — it's learning general fault patterns, not memorizing specific units.  
     
    \- \*\*H4b:\*\* The anomaly score isn't secretly just tracking the weather, how long it's been since cleaning, or which physical kit took the reading.  
     
  \*\*Hypothesis Execution Order & Dependencies\*\* (for planning; draft stays in RQ reading order):  
     
  \*\*First to test — H1a (gate):\*\* If no sensor group separates known-fault from known-healthy, the entire sensor suite is in question. Test with a baseline model \+ Layer 1 retrospective data before investing in Phase 7 CNN / PCA / PMV.  
 


- [x] 🔴 **Reframe positioning as complementary triage** — `1.1 COLLIN ASIO`  
  *→ This heads off the natural misreading that the system replaces PPO's maintenance schedule — it frames the system as helping PPO prioritize which units to check between cleanings, not a replacement for cleaning.*  
     
     
  \- Explicitly state: this system does NOT replace scheduled preventive maintenance. It is a diagnostic layer that flags which units need attention between cleanings, helping the PPO prioritize inspections.    
     
  \- Reference the maintenance logs as evidence that faults have been observed between scheduled cleanings (e.g., "13-MAR-23 LEAK REPAIR & REPLACEMENT OF OUTDOOR FAN MOTOR").    
     
  \- Pitch as proof-of-concept for Campus of the Future implementation.  
     
- [x] 🟠 **Strengthen RA 11285 rationale** — `1.1 SIMON SULIBIO`  
  *→ RA 11285 is the Philippine energy-efficiency law the thesis leans on for justification — this adds an actual peso-value energy-waste estimate so the economic argument has real numbers, not just an appeal to the law.*  
     
     
  \- Add quantified energy savings estimate: "30 units × avg 2.5kW × 2,000 hrs/yr × 6.4% fouling penalty (Niknami et al., 2024\\) × ₱12/kWh ≈ ₱115,000 annual waste. Early detection could reduce this."  
     
- [x] 🟠 **Update scope and limitations for non-invasive approach** — `1.5 SIMON SUILBIO`  
  *→ Scope and limitations tell the reader exactly what this study does and doesn't claim, keeping expectations honest while still setting up the larger "Campus of the Future" vision without overpromising.*  
     
     
  \- Scope: non-invasive external sensors only; 30-40 units across 3 locations; weekly visits with 2 portable kits (proof-of-concept phase); anomaly detection as triage tool. \*\*Long-term vision:\*\* permanent sensor module installed per AC unit (Campus of the Future), continuously monitoring with automated anomaly alerts — this thesis validates the core approach.    
     
  \- Acknowledge: cannot directly observe evaporator coil condition; model detects proxy signals, not faults themselves; weekly sampling may miss transient failures between visits; portable kit mounting introduces measurement variability (mitigated by standardized protocol \\+ kit ID tracking).    
     
  \- State explicitly: fault injection during validation is part of experimental design, not operational deployment. The deployed system remains non-invasive; invasive inspection is only for labeling during the study and for controlled fault injection.  
     
- [x] 🟡 **Justify unsupervised over supervised** — `1.5 or 3.3 COLLIN ASIO`  
  *→ Reviewers will ask "why not just train a normal classifier?" — this pre-empts that with the actual math: 13 known-fault units out of 2,599 campus-wide is too few labels for supervised learning to be reliable.*  
     
     
  \- Walk the reader through the data constraint: 13 known-problem units out of 2,599 campus-wide. In a 30-40 unit sample, expect 0-3 naturally occurring Abnormal observations. Supervised classification with 0-3 positive examples is statistically unvalidatable.    
     
  \- Unsupervised anomaly detection trains on abundant normal data (\\\~95%+ of data), learns the operating envelope, and flags deviations — matching the triage framing exactly.    
     
  \- Mention: supervised classification will be tested as a secondary experiment IF controlled fault injection produces enough labeled samples (30+).  
     
- [x] 🟢 **Add scope diagram** — `1.5 SIMON SULIBIO`  
  *→ A single visual showing what's in scope vs. out of scope makes the boundaries from the previous task easy to grasp at a glance instead of piecing them together from prose.*  
     
     
  \- Visual: in scope vs. out of scope. Non-invasive anomaly detection as focus.

### Chapter 3 — Methodology (Pre-Prototyping Sections)

- [ ] 🔴 **Research Design Overview** — `3.1.1 COLLIN ASIO`

  Trim the design-classification paragraph — state up front that this is an Experimental Research Design (controlled, instrumented, repeated-trial collection) in the first 2–3 sentences, then cut the restated justification later in the paragraph that just re-argues the same point. Reconcile two mismatches against your locked decisions before finalizing: 

* **Sensor list** — this draft still names ACS712 and ZMPT101B; those are replaced by the SCT-013 Split Core CT (30A/1V), voltage sensing dropped.   
* **ML model list** — this draft says CNN, Random Forest, XGBoost, k-NN, RBF SVM, and DNN will be compared. That's the old supervised-comparison framing; the approved architecture is unsupervised-primary (Autoencoder, Isolation Forest, One-Class SVM, GMM), with the supervised secondary experiment dropped. Worth checking whether this section is from before that decision.  
* Keep as-is: the 6-month/weekly-visit cadence, 30–40 unit rotation across CoE/Faber Hall/SBM-AVR, and the 10-trials-per-unit @ 1 min/10 Hz (600 samples/sensor/trial) protocol — all consistent with the approved plan.   
    
    
- [ ] 🔴 **Update sources of Data** — `3.1.2 JOHN PACALDO`	

  Explain how each data will be collected:

* ambient temp mean  
* ambient temp std  
* ambient rh mean  
* ambient rh std  
* inlet temp mean  
* inlet temp std  
* outlet temp mean  
* coil temp std  
* delta T mean   
* delta T std  
* current mean  
* current std  
* airflow mean  
* airflow std  
* Vibration rms  
* Vibration kurtosis  
* Vibration peak frequency

	Explain the metadata also:

* unit\_id  
* Unit\_type  
* Vistit\_id

- [ ] 🔴 **Update Sampling Areas** — `3.1.3 JOHN PACALDO`

  Structure stays fine as purposive sampling with a numbered per-location breakdown; keep that format. A few things worth reconciling against the roadmap before finalizing:

* **Sample size mismatch** — this draft says "a maximum of 50" units, but the roadmap and risk registry both target **30–40** units (with a fallback of starting at 20 and expanding if the 2-kit weekly rotation can't keep up). Confirm whether 50 is an intentional revision or should be pulled back to 30–40.  
* **Missing prioritization criterion** — Phase 6 specifies prioritizing **"With Concern" units and split-type over window-type**. This section's rationale (operational hours/humidity for AVR, accessibility for CoE, "complete the sample size" for Faber Hall 1st floor) is about access and uniformity, not fault-likelihood. Worth adding a line on how "With Concern" units get identified/prioritized within each location, or noting if that criterion was dropped.  
* **Faber Hall rationale reads as an afterthought** — "additional units... to complete the needed sample size" may want a stronger justification (e.g., why 1st floor specifically, what makes those units comparable to the other two sites) so it doesn't look like padding to a panel.  
    
    
- [ ] 🔴 **Nested: 🔧 Hardware BOM finalization** — `3.1.4 COLLIN ASIO`  
  Update Electrical and Vibration Node Kit: SCT-013 Split Core Current Transformer will be used instead of ACS712 and ZMPT101B. SCT-013 will only monitor the power and current input. MPU6050 will still be used for the vibration.

- [ ] 🟠 **Add system architecture diagram** — `3.1.4 JOHN PACALDO` *→ One diagram showing the full data path — sensor nodes → Master ESP32 → laptop → CSV → pipeline — so a reader can see how the pieces fit together without reading every hardware and software section separately.*  
     
  \- 2 node types (Thermal \\+ Electrical/Vibration) → Master ESP32 (ESP-NOW) → Laptop/Server (Serial) → CSV → preprocessing pipeline.

  \\- No ESP32-CAM, no Frost Node, no Wi-Fi image upload.


  \\- Power source per node, communication paths, data flow.


- [ ] 🟡 **Add power management plan** — `3.1.4 SIMON SULIBIO`  
  *→ Each kit needs to run through a full day's 10 trials without dying mid-visit — planning how it's powered, and for how long, keeps a dead battery from quietly corrupting a day's data.*  
     
     
  \- Power source per node (USB power bank, wall outlet, or AC unit tap).    
     
  \- Battery life estimate for portable operation.    
     
  \- Sleep/wake cycles if needed for energy optimization.

- [ ] 🟠 **Add Kicad schematics**  — `3.1.4 JOHN PACALDO` 

- ***Articuno and Moltres***  
- ***Zapdos and Regigas***  
- ***Tornadus***  
- ***Rayquaza***   
     
- [ ] 🔴 **Add sampling parameters table** — `3.1.5 JOHN PACALDO`  
  *→ Turns the sampling rates and durations into one reference table (e.g. 5,400 readings/unit/visit from the 9 non-vibration sensors) so later chapters can point back to it instead of re-deriving the numbers each time.*  
     
   \- Check Claude for the Sampling: Explain how the definition of terms, and the data points or window collected from each unit. How many units will be used, and etc.   
   

- [ ] 🟡 **Standardize portable kit mounting protocol** — `3.1.5 COLLIN ASIO`  
  *→ Since the same 2 kits get physically moved between 30-40 different units, inconsistent probe placement from visit to visit would be a hidden source of noise — this writes down the exact placement so readings stay comparable.*  
     
     
  \- Document exact probe placement per sensor type.    
     
  \- Include Kit ID as a model development feature (to detect kit-driven bias), exclude from the final model.    
     
  \- Verify kit-to-kit calibration before each deployment day.


- [ ] 🟠 **Define labeling and validation protocol** — `3.1.6 COLLIN ASIO`

  **Training Phase (Unsupervised Baseline)** — no changes needed. Matches the approved architecture as-is.

  **Validation Layer 1: Retrospective Historical Comparison** — **remove this subsection entirely.** This is the layer that got dropped for lack of time to verify the 13 units' current status with PPO. Leaving it in would directly contradict a decision already made.

  **Validation Layer 2: Controlled Fault Injection** — keep, but **renumber to "Validation Layer 1"** (it's now first in the 4-layer sequence), and fix two things:

* To test the system's diagnostic reliability and sensitivity, controlled physical faults will be deliberately introduced on 2 to 3 test units. These actions include blocking the return air, reducing refrigerant via a licensed technician, and temporarily misaligning the fan. Each unit's readings are recorded before and after the intervention as a paired sample. The model's reliability is confirmed on two fronts: first, that the anomaly score shows a statistically significant rise between the paired pre- and post-injection readings, tested via Wilcoxon signed-rank (H1a, p\<0.05); and second, that the model achieves a True Positive Rate of ≥80% in flagging the injected faults (H2a). 

- [ ] 🟠 **Define Validation Procedures for each sensor (Calibration Procedures)**— `3.1.6 SIMON SULIBIO`

  **Validity Experiment (currently blank)** — same gap flagged before, now more specific:

* **BME280 / DS18B20** — no calibration method documented anywhere yet; needs one written here.  
* **SCT-013 (30A/1V)** — this is the one sensor whose calibration method is still genuinely undecided post-hardware-swap. This section is the right place to lock it down.  
* **MPU6050** — already calibrated (offsets: AX\_BIAS=-0.005124, AY\_BIAS=-0.265409, AZ\_BIAS=0.379842) — just restate, don't re-derive.

- [ ] 🔴 **Add unsupervised methodology justification** — `3.3 JOHN PACALDO`  
  *→ Explains what each of the four chosen models actually does (Autoencoder, Isolation Forest, One-Class SVM, GMM) and why alternatives like k-NN and DNN were dropped — the technical companion to the earlier "justify unsupervised" task.*  
     
     
  \- Primary: 4 unsupervised models (Autoencoder, Isolation Forest, One-Class SVM, GMM).    
     
  \- Autoencoder: learns to reconstruct normal sensor readings; reconstruction error above threshold \\= anomaly.    
     
  \- Isolation Forest: isolates anomalous points efficiently; non-parametric, suited to mixed feature types.    
     
  \- One-Class SVM: learns decision boundary around normal data; kernel-based.    
     
  \- GMM: probabilistic model; likelihood scores for anomaly scoring.    
     
  \- Secondary (conditional): RF, XGBoost, RBF SVM if fault injection produces ≥30 labeled samples. Drop k-NN and DNN from primary lineup.  
 


- [ ] 🔴 **Add Experimental Procedures of the Hypotheses** — `3.1.7 JOHN PACALDO`  
- Explain how the experiment of hypotheses 1 would work.  
- Explain how the other experiments work. 

    
     
     
     
    
    
    
    
    
    
    
    
  


---

## Phase 2 — Prototyping: Hardware Validation

**Goal:** Assemble and test 2 complete portable sensor kits. Verify all sensors read correctly, ESP-NOW communication is stable, and the Master ESP32 outputs structured CSV data.

**In plain terms:** This is the "does the hardware actually work" phase — assembling both kit types, getting every sensor reading correctly, and confirming they can wirelessly relay data back to a receiver reliably, before committing six months of fieldwork to them.

### Sensor Nodes

- [ ] 🔴 **🔧 Assemble Thermal Node prototype (×2)** — `ambient_module_final/`  
  *→ The first kit type gets physically built — temperature/humidity plus the three surface probes wired to an ESP32-C3 — so it can be tested before months are spent trusting its readings.*  
     
     
  \- ESP32-C3 \\+ BME280 (I2C 0x76) \\+ 3× DS18B20 (OneWire GPIO10).    
     
  \- Verify all 4 sensors read simultaneously.    
     
  \- Apply calibration factors as hardcoded constants.    
     
  \- Serial output: \`Temp=XX.X Hum=XX.X Counter=X A=XX.X B=XX.X C=XX.X\`.  
     
- [ ] 🔴 **🔧 Assemble Electrical/Vibration Node prototype (×2)**  
  *→ The second kit type — current, voltage, and vibration — is kept as a separate physical unit so a fault in one node type (e.g. an electrical short) can't take down the temperature readings too.*  
     
     
  \- ESP32-C3 \\+ 2× ACS712 \\+ ZMPT101B \\+ MPU6050.    
     
  \- Verify current and voltage readings with reference DMM at XU ME/EE labs.    
     
  \- Measure and record zero-current offset for both ACS712 channels.    
     
  \- Test MPU6050 vibration capture at 100 Hz; verify spectrogram conversion.  
     
- [ ] 🔴 **🔧 Verify MPU6050 calibration offsets**  
  *→ The vibration sensor has small built-in biases even at rest — checking these now keeps the Phase 7 vibration model from being quietly biased before it even starts.*  
     
     
  \- From calibration CSV: AX\\\_BIAS \\= \\-0.005124, AY\\\_BIAS \\= \\-0.265409, AZ\\\_BIAS \\= 0.379842.    
     
  \- Apply in firmware as hardcoded constants.

### ESP-NOW Communication

*What this covers: getting the wireless link between sensor nodes and the receiver working reliably, and time-aligning readings from both node types.*

- [ ] 🔴 **🔧 ESP-NOW master-slave pairing**  
  *→ Confirms the wireless link between each sensor node and its receiver is actually stable — if this doesn't work reliably, no data gets collected at all, so it's tested early rather than discovered mid-fieldwork.*  
     
     
  \- 2 senders (Thermal, Electrical/Vibration) → 1 Master ESP32.    
     
  \- Test channel scanning via SSID \`PLDTHOMEFIBRd2228\`; fallback channel 11\\.    
     
  \- Verify MAC addresses: Sender 1 \`E0:72:A1:72:22:94\`, Sender 2 \`E0:72:A1:72:29:00\`, Receiver \`E0:72:A1:6F:F8:6C\`.    
     
  \- Test 3-second send interval stability over 1-hour continuous run.    
     
  \- \*\*ESP-NOW receive callback must only set a flag\*\* (\`volatile bool newDataReady\`). Processing runs in \`loop()\` — never in ISR.  
     
- [ ] 🟠 **🔧 Timestamp synchronization protocol**  
  *→ The two node types send readings independently — they need a shared, reliable timestamp so a temperature reading and a vibration reading from the same moment can actually be lined up later.*  
     
     
  \- Master broadcasts sync pulse → both nodes timestamp readings.    
     
  \- Verify both nodes report same timestamp within ±50ms tolerance.  
     
- [ ] 🟡 **🔧 Data struct validation**  
  *→ Checks that the data packet format sent over ESP-NOW actually matches what the receiving code expects, so nothing gets silently dropped or misread on the way in.*  
     
     
  \- Verify \`EspNowPacket\` struct (type \\+ 6 floats) matches across all nodes.    
     
  \- Test edge cases: NaN values, sensor disconnect (default to 0.0 or \\-999.0).

### TFT Display UI (Optional)

- [ ] 🟡 **🔧 TFT complete UI** — `tft_complete/`  
  *→ The optional on-kit screen lets whoever's carrying the kit confirm readings are coming through correctly during a visit, without needing to check a laptop.*  
     
  \- ST7789 240×320 SPI \+ XPT2046 touch.  
  \- Pages: Main Menu → Pairing → Devices → Units → System.  
  \- Display live sensor data from Master ESP32 via Serial/UART.

### Firmware Coding

- [ ] 🔴 **💻 Calibration factor integration**  
  *→ Bakes the calibration math from Phase 4 directly into the firmware, so the kit reports already-corrected values instead of raw numbers that would need fixing later.*  
     
     
  \- Embed verified calibration constants in all sensor sketches:    
     
    \- BME280: \`T\_cal \= T\_raw × 1.0294412\`, \`H\_cal \= H\_raw × 1.0579399\`    
     
    \- DS18B20 A: \`1.701471 \+ 0.984997 × raw\`    
     
    \- DS18B20 B/C: \`1.637417 \+ 0.9783362 × raw\`    
     
    \- MPU6050: apply AX/AY/AZ bias offsets    
     
  \- ACS712: \`ADC\_raw − ADC\_Zero\_Offset\` → calibrated current via sensitivity factor.  
     
- [ ] 🟠 **💻 Data formatting script**  
  *→ Converts whatever comes off the Serial connection into clean, structured CSV rows, since raw serial output usually isn't immediately usable as a dataset.*  
     
     
  \- Master ESP32 outputs structured CSV line: \`timestamp,unit\_id,set\_temp,temp,humid,pressure,inlet,outlet,coil,comp\_current,fan\_current,voltage,accel\_x,accel\_y,accel\_z\`.    
     
  \- Ingest script: reads Serial, validates format and ranges, writes to \`02\_Data/raw/\` with naming convention: \`YYYYMMDDTHHmmSSZ\_\<Location\>\_\<UnitID\>\_\<TrialNum\>\_RAW.csv\`.

### Nested Paper Tasks

- [ ] 🟡 **📝 Update Chapter 3** from prototyping learnings  
  *→ Once hardware is actually built and tested, this folds back anything that turned out different from the original plan into the methodology chapter, so the paper matches what was really built.*  
     
  \- Record actual vs. expected sensor accuracy.  
  \- Document hardware substitutions and deviations from plan.  
  \- Update system architecture diagram with final wiring and confirmed sensor lineup.

---

## Phase 3 — Paper Overhaul: Literature & Gaps

**Goal:** Overhaul Chapter 2 (RRL) with a synthesis matrix, replacement of tangential studies, and alignment with the unsupervised anomaly detection methodology.

**In plain terms:** With the non-invasive, unsupervised direction locked in Phase 1, the literature review needs to actually support that direction — this phase swaps out sources that no longer fit and builds the comparison table showing where this thesis sits relative to prior work.

### Chapter 2 — Review of Related Literature

- [ ] 🔴 **📝 Add synthesis matrix** — `2.11 (new section)`  
  *→ Instead of summarizing sources one after another, this builds a table comparing them side-by-side — the standard way to show exactly where this thesis's approach differs from what's already been done.*  
     
     
  \- Multi-dimensional comparison table: Study \| Model \| Dataset size \| Accuracy \| Sensor types \| HVAC type \| Deployment context \| Limitation.    
     
  \- Column for supervised vs. unsupervised approach.    
     
  \- Write 3-5 explicit research gaps this thesis addresses, including: "limited application of unsupervised anomaly detection in non-invasive HVAC condition monitoring using low-cost external sensors."  
     
- [ ] 🔴 **📝 Replace tangential studies**  
  *→ Two previously-cited studies don't actually fit the non-invasive, unsupervised direction — swapping them for more directly relevant HVAC studies keeps the literature review honestly supporting the thesis.*  
     
     
  \- Remove 2.8 (Aji et al., magnetic sensors — not HVAC).    
     
  \- Remove 2.9 (Abood et al., electromechanical motors — not HVAC).    
     
  \- Replace with:    
     
    \- Study on unsupervised anomaly detection for building/HVAC systems (expand Bouabdallaoui et al., 2021 — 2.5).    
     
    \- Study on low-cost sensor calibration for predictive maintenance.    
     
    \- Study on evaporator coil fouling detection via proxy signals (expand Niknami et al., 2024 — already cited in Chapter 1).  
     
- [ ] 🟠 **📝 Reconcile calibration formula with literature**  
  *→ Makes sure the calibration math from Phase 4 is presented consistently with how similar calibrations appear in the cited literature, so the methodology doesn't look inconsistent with its own references.*  
     
     
  \- Fix Probe B regression output in Chapter 4: either update R output screenshot or correct stated formula. Verify all calibration formulas match firmware codebase exactly.    
     
  \- Fix Probe A data error (\`17.3\` → \`27.3\`) in appendix.  
     
- [ ] 🟡 **📝 Cite foundational ML papers**  
  *→ Each of the four chosen models comes from a specific original paper (e.g. Isolation Forest → Liu et al. 2008\) — citing these grounds the model choices in established, peer-reviewed work.*  
     
     
  \- Breiman (2001) for Random Forest. Chen & Guestrin (2016) for XGBoost. Cortes & Vapnik (1995) for SVM. Liu et al. (2008) for Isolation Forest. Schölkopf et al. (2001) for One-Class SVM.    
     
     
  \- Don't rely solely on Sarker (2021) for all algorithm descriptions.  
     
- [ ] 🟡 **📝 Add conceptual framework diagram from literature**  
  *→ Shows visually how this thesis relates to the broader body of related work, tying the literature review back to the framework introduced in Chapter 1\.*  
     
     
  \- Visual: literature findings → informs this thesis architecture.    
     
  \- Highlight unique contribution: ESP32 \\+ ESP-NOW \\+ low-cost external sensors \\+ unsupervised anomaly detection as triage tool.

### Nested ML Tasks

- [ ] 🟠 **🤖 Final model selection with justification**  
  *→ Puts the final, locked-in model list in the literature review with a stated reason for each — the last checkpoint before Phase 5 starts writing detailed architectures for them.*  
     
  \- **Primary (unsupervised):** Autoencoder (deep learning; reconstruction error), Isolation Forest (tree-based; non-parametric; well-suited to small-medium data), One-Class SVM (kernel-based; comparison baseline), GMM (probabilistic; confidence scores).  
  \- **Secondary (supervised, conditional):** RF, XGBoost, RBF SVM — only if fault injection produces ≥30 labeled samples. Justification: supervised comparison experiment validates whether labeled data improves over unsupervised when labels are available.  
  \- **Dropped:** k-NN (rarely competitive at this sample size), DNN (insufficient training data — require hundreds to thousands of labeled examples), ESP32-CAM CNN (removed — non-invasive constraint).

---

## Phase 4 — Sensor Calibration: Remaining Sensors

**Goal:** Complete calibration of ACS712 and ZMPT101B sensors using equipment available at XU ME/EE labs. Build the calibration database for automated CCF application.

**In plain terms:** Two sensors (current and voltage) don't come pre-calibrated — their raw electrical readings have to be matched against a trusted reference instrument so the numbers they report can be trusted as real amps and volts, not arbitrary sensor units.

### ACS712 Current Calibration

*What this covers: working out the exact math (zero point \+ scaling factor) that turns each ACS712's raw reading into a real current value in amps.*

- [ ] 🔴 **📊 Zero-offset calibration** — both ACS712 channels  
  *→ The ACS712 current sensor reads a nonzero value even at 0 amps — finding that baseline offset for each channel means it can be subtracted out, otherwise every reading would be off by a constant amount.*  
     
     
  \- Node powered on, no load connected.    
     
  \- 1,000 ADC readings over 60 seconds per sensor.    
     
  \- Compute: \`ADC\_Zero\_Offset \= mean(1,000 readings)\`.    
     
  \- Store per-sensor UID in calibration database (\`01\_Sensor\_Calibration/\`).  
     
- [ ] 🔴 **📊 Sensitivity (gain) calibration**  
  *→ Determines exactly how many volts the sensor outputs per amp of current, using known reference loads — without this scaling factor, raw readings can't be converted into real amps at all.*  
     
     
  \- Connect known resistive loads: 50W, 200W, 250W bulbs.    
     
  \- Measure True-RMS current with reference DMM at XU ME/EE labs.    
     
  \- Linear regression per sensor: \`I\_actual \= m × (ADC\_raw − ADC\_Zero\_Offset) \+ c\`.    
     
  \- If non-linear at low currents (fan motor range 0-1A) → use piecewise or polynomial fit.

### ZMPT101B Voltage Calibration

*What this covers: the equivalent calibration process for the voltage sensor — a curve fit instead of a straight line, since this sensor isn't linear across its whole range.*

- [ ] 🔴 **📊 Trimpot standardization**  
  *→ The ZMPT101B has a physical adjustment screw that varies unit to unit — setting it to a known position ensures both kits' voltage sensors start from the same baseline instead of behaving slightly differently.*  
     
     
  \- Adjust onboard potentiometer: 250V input → ADC output \\\~640 (below saturation, provides headroom).    
     
  \- Standardize across both Electrical/Vibration Node kits.  
     
- [ ] 🔴 **📊 3rd-order polynomial calibration**  
  *→ Unlike the current sensor, this one's output isn't a straight line against real voltage — a curve fit across 50-250V is needed to convert its raw reading into an accurate voltage value across the whole range.*  
     
     
  \- Variac: 10 voltage setpoints from 50V to 250V.    
     
  \- Record ADC reading vs. True-RMS DMM reference.    
     
  \- Fit 3rd-order polynomial per module: \`V\_actual \= a₀ \+ a₁·ADC \+ a₂·ADC² \+ a₃·ADC³\`.    
     
  \- Report R² and max absolute error.

### Calibration Database

- [ ] 🟠 **💻 Calibration database script**  
  *→ Stores every calibration constant in one place (a JSON file) with a lookup function, so the rest of the codebase doesn't hardcode calibration numbers in multiple places.*  
     
     
  \- JSON per sensor type: \`{UID: {type: "linear"\|"polynomial", coefficients: \[...\]}}\`.    
     
  \- Version control in \`01\_Sensor\_Calibration/\`.    
     
  \- Python helper: \`apply\_ccf(uid, raw\_value) → calibrated\_value\`.  
     
- [ ] 🟡 **💻 Automated CCF application**  
  *→ Wires the calibration database into the data pipeline so every raw reading gets automatically corrected as it comes in, instead of applying the formula to each row by hand.*  
     
     
  \- Preprocessing pipeline reads raw CSV → looks up UID → applies CCF → writes to \`02\_Data/interim/\`.    
     
  \- Unit test: known raw value → verify calibrated output matches expected.

### Nested Paper Tasks

- [ ] 🟠 **📝 Write Chapter 4 sensor calibration results**  
  *→ Documents the actual calibration curves, constants, and accuracy achieved — the evidence a reviewer would want that the sensors were properly validated before six months of fieldwork relied on them.*  
     
  \- Per sensor: scatter plot (sensor vs. reference with regression line \+ 95% CI band).  
  \- Per sensor: residual plot. Q-Q plot for residual normality.  
  \- Report R², RMSE, max error on held-out validation set (80/20 train/val split per sensor type).  
  \- Include uncertainty discussion: residual std error per sensor, whether accuracy is sufficient for anomaly detection.  
  \- Fix Probe A data error (`17.3` → `27.3`) before any analysis.  
  \- Reconcile Probe B formula (regression output must match stated formula in Ch4 and firmware).

---

## Phase 5 — Paper Overhaul: Methodology Details

**Goal:** Condense the \~40-page textbook content in Chapter 3.3. Replace supervised classification architectures with unsupervised anomaly detection model definitions. Define validation strategy in detail.

**In plain terms:** This is where the four candidate models get fully specified on paper — what data goes in, what architecture each uses, what settings will be tried, and how "did it work" will be measured — before any of them are actually coded and trained in Phase 8\.

- [ ] 🔴 **📝 Condense Chapter 3.3 Model Development section**  
  *→ The existing draft over-explains generic machine-learning theory like a textbook chapter — trimming it keeps the methodology focused on this thesis's specific choices rather than general ML background.*  
     
     
  \- Cut textbook content: move linear regression, gradient descent, backpropagation derivations to Appendix.    
     
  \- Keep in main text: 1-2 paragraph summary per model \\+ architecture specification table.  
     
- [ ] 🔴 **📝 Define unsupervised model architectures**  
  *→ Specifies exactly how each of the four primary models is built and what "anomaly" means for each (e.g. reconstruction error for the Autoencoder, likelihood for GMM) — the blueprint Phase 8 will code from.*  
     
     
  \- \*\*Autoencoder:\*\* Input (9 sensor features: set\\\_temp \\+ 8 calibrated sensor readings) → Encoder (Dense 64 ReLU → Dense 32 ReLU → Dense 16 latent) → Decoder (Dense 32 ReLU → Dense 64 ReLU → Dense 9 linear). Reconstruction error (MSE) as anomaly score. Threshold: 95th percentile of training reconstruction error.    
     
  \- \*\*Isolation Forest:\*\* n\\\_estimators \\\[100, 200, 500\\\], contamination \\\[auto, 0.01, 0.05, 0.10\\\], max\\\_samples \\\[256, auto\\\]. Anomaly score: path length.    
     
  \- \*\*One-Class SVM:\*\* kernel \\\[RBF\\\], nu \\\[0.01, 0.05, 0.10\\\], gamma \\\[scale, auto, 0.01, 0.1\\\]. Anomaly score: signed distance from decision boundary.    
     
  \- \*\*GMM:\*\* n\\\_components \\\[1, 2, 3, 5, 10\\\] (selected via BIC). Anomaly score: negative log-likelihood.  
     
- [ ] 🔴 **📝 Define CNN spectrogram anomaly detection architecture**  
  *→ Does the same detailed specification for the separate vibration model from Phase 7 — a different kind of model (a convolutional network on images) that needs its own architecture write-up.*  
     
     
  \- Input: MPU6050 vibration → spectrogram image (time-frequency representation).    
     
  \- Architecture: Transfer learning (MobileNetV2 pretrained on ImageNet), fine-tuned on vibration spectrograms.    
     
  \- Approach: Convolutional Autoencoder — learns to reconstruct spectrograms of normal vibration patterns. Reconstruction error above threshold \\= anomalous vibration.    
     
  \- Vibration anomaly score → concatenated with sensor features in final anomaly model OR used as a multimodal anomaly detection branch.    
     
  \- Explicitly justify ImageNet weights: not an external HVAC dataset — a general-purpose computer vision foundation model, which is standard practice.  
     
- [ ] 🟠 **📝 Specify hyperparameter search space** per model  
  *→ Lists which settings (tree depth, outlier-fraction, etc.) will be tried during training, so model tuning in Phase 8 follows a plan instead of ad hoc guessing.*  
     
     
  \- Isolation Forest: n\\\_estimators \\\[100, 200, 500\\\], contamination \\\[0.01, 0.05, 0.10\\\].    
     
  \- One-Class SVM: nu \\\[0.01, 0.05, 0.10\\\], gamma \\\[scale, auto, 0.01, 0.1\\\].    
     
  \- GMM: n\\\_components \\\[1, 2, 3, 5, 10\\\], covariance\\\_type \\\[full, tied, diag, spherical\\\].    
     
  \- Autoencoder: latent\\\_dim \\\[8, 16, 32\\\], learning\\\_rate \\\[0.001, 0.0001\\\], epochs \\\[50, 100\\\], batch\\\_size \\\[32, 64\\\].  
     
- [ ] 🟡 **📝 Add overfitting mitigation section**  
  *→ States upfront how the study guards against a model that just memorizes the specific 30-40 units it saw rather than learning general patterns — this is what the Leave-One-Unit-Out test (H4a) later checks.*  
     
     
  \- Autoencoder: L2 regularization, dropout in encoder, early stopping (patience=10).    
     
  \- Isolation Forest: max\\\_samples, limited tree depth.    
     
  \- One-Class SVM: nu parameter controls outlier fraction.    
     
  \- GMM: BIC for model selection.  
     
- [ ] 🟡 **📝 Define evaluation metrics for unsupervised models** — map to H1a–H4b  
  *→ Maps every H1a-H4b hypothesis to a specific statistical test and pass threshold — the scoreboard without which "success" would be subjective rather than checkable.*  
     
     
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
  *→ Gets a consistent, reproducible coding environment running before anyone writes model code, so results aren't affected by different team members using different library versions.*  
     
     
  \- Activate venv: \`cd "codes/python/machine learning"; python \-m venv .venv; .venv\\Scripts\\Activate.ps1\`.    
     
  \- Install deps: \`pip install \-r ../requirements.txt\`.    
     
  \- Verify: \`python \-c "import numpy, matplotlib, sklearn, pandas, torch; print('OK')"\`.  
     
- [ ] 🟡 **💻 Project scaffolding**  
  *→ Sets up the folder structure and a central config file before real coding starts, so file organization doesn't become chaotic once multiple people are writing code in parallel.*  
     
     
  \- Create \`03\_Code/\` directory structure (ingest, preprocessing, modeling, evaluation subdirs).    
     
  \- Initialize Git for code tracking.    
     
  \- Create \`config.yaml\` for paths, parameters, model configs, anomaly thresholds.

---

## Phase 6 — Data Collection

**Goal:** Deploy 2 portable kits across 30-40 units at 3 locations over 6 months. Collect consistent, calibrated sensor data. Apply weekly labeling protocol for validation.

**In plain terms:** This is the actual fieldwork — six months of weekly visits carrying the two kits to 30-40 real AC units, plus a few sessions where faults are deliberately introduced so there's guaranteed "bad" data to test the models against later.

### Hardware Deployment

- [ ] 🔴 **📊 Finalize 30-40 unit sample**  
  *→ Locks down which specific AC units will actually be studied, prioritizing units already flagged with concerns and split-type units — this shapes every visit for the next six months.*  
     
     
  \- Select units from SBM-AVR, College of Engineering, Faber Hall 1st floor.    
     
  \- Prioritize units with "With Concern" status from maintenance logs to maximize abnormal data.    
     
  \- Prioritize split-type units (CM, CT, WM types) over window-type (WRAC).    
     
  \- Pull cleaning dates from PPO maintenance logs for each selected unit.  
     
- [ ] 🔴 **📊 Weekly data collection sessions** — 6 months  
  *→ This is the actual six-month data-gathering routine itself — the core fieldwork everything else in the thesis depends on having real data from.*  
     
     
  \- 2 kits, one location per day, rotate through all units.    
     
  \- Each visit: 10 trials per unit.    
     
  \- Each trial: 1 minute of continuous readings at 10 Hz (sensors) \\+ 100 Hz (MPU6050).    
     
  \- Record per trial: set temperature (manually read from thermostat/remote), ambient temp, humidity, pressure, inlet/outlet/coil temp, compressor/fan current, supply voltage, 3-axis acceleration.    
     
  \- Compute time-since-last-cleaning per unit per visit from maintenance logs.  
     
- [ ] 🟠 **📊 Controlled fault injection validation** — 3 sessions during study  
  *→ Since naturally-occurring faults are rare, this deliberately creates a few faults under controlled conditions so there's guaranteed before/after data proving the anomaly score reacts to real problems.*  
     
     
  \- With campus facilities permission, induce controlled faults on 2-3 units per session:    
     
    \- Partially block return air grille (simulate fouling/obstruction).    
     
    \- Reduce refrigerant charge via service valve (requires licensed technician — one-time supervised procedure).    
     
    \- Misalign fan blade (simulate mechanical imbalance).    
     
  \- Protocol: baseline measurement → induce fault → post-fault measurement → restore → recovery measurement.    
     
  \- Label each phase explicitly. This creates known ground truth for model validation.  
     
- [ ] 🟠 **📊 Monthly technician spot-checks** — validation layer  
  *→ Has an HVAC technician periodically look at a subset of units and give an independent opinion — this is Validation Layer 3, a human sanity-check against what the model reports.*  
     
     
  \- Rotating subset: 5-8 units per month.    
     
  \- Brief visual inspection checklist: abnormal vibration, poor cooling, unusual current, excessive noise, visible external issues.    
     
  \- Record findings. Correlate with anomaly scores at end of study.

### Data Pipeline

- [ ] 🔴 **💻 Data ingestion script**  
  *→ Automates pulling raw CSV files off the kits into wherever the pipeline expects them, so data doesn't have to be moved and organized by hand after every visit.*  
     
     
  \- Reads Serial from Master ESP32.    
     
  \- Validates format (expected columns, ranges).    
     
  \- Writes to \`02\_Data/raw/\` with naming convention: \`YYYYMMDDTHHmmSSZ\_\<Location\>\_\<UnitID\>\_\<TrialNum\>\_RAW.csv\`.  
     
- [ ] 🟠 **💻 Data cleaning & CCF application**  
  *→ Runs the calibration correction and basic cleanup (removing corrupted rows, handling planned sensor failures) on raw incoming data before it's usable for anything else.*  
     
     
  \- Script reads \`02\_Data/raw/\` → applies CCFs from \`01\_Sensor\_Calibration/\` → validates ranges → writes to \`02\_Data/interim/\`.    
     
  \- Handles missing values: forward-fill short gaps (\\\< 5 readings), flag longer gaps with indicator column.    
     
  \- Detects and flags outliers (outside 3σ or manual engineering thresholds).  
     
- [ ] 🟠 **💻 Feature engineering** for interim → processed  
  *→ Turns cleaned raw readings into the actual input variables the models will use — the step that translates sensor data into something a model can learn from.*  
     
     
  \- Rolling window statistics per trial: mean, std, min, max, slope.    
     
  \- Rate-of-change features: Δ(Inlet−Outlet)/Δt, ΔCoilTemp/Δt.    
     
  \- Derived COP proxy: (Inlet − Outlet) / Compressor Current.    
     
  \- Derived target delta-T: (Set Temp − Outlet Temp) — positive delta indicates AC is meeting target; negative delta indicates degradation.    
     
  \- Vibration statistical features: RMS, peak amplitude, spectral kurtosis, dominant frequency.    
     
  \- Vibration spectrogram generation: FFT → time-frequency image saved per trial.    
     
  \- Time-since-last-cleaning: computed from maintenance log cleaning dates.    
     
  \- Kit ID: included during development, excluded from final model.  
     
- [ ] 🟡 **💻 Data validation dashboard** (optional)  
  *→ An optional visual check to quickly spot problems in incoming data during the six-month study, rather than only discovering data quality issues later during modeling.*  
     
     
  \- Simple Streamlit page: per-unit data completeness, sensor health, weekly trial count.    
     
  \- Alerts if unit has \\\< 10 trials in a week.

### Nested Paper Tasks

- [ ] 🟡 **📝 Update Chapter 3 DMP section**  
  *→ Once real fieldwork has started, this documents the actual data-management practices being followed as they're really implemented, not just as originally planned.*  
     
  \- Replace theoretical DMP with actual implementation notes.  
  \- Record deviations from planned storage/backup strategy.  
  \- Document actual file counts and data volumes.

---

## Phase 7 — Machine Learning: Vibration CNN

**Goal:** Train a convolutional autoencoder on MPU6050 vibration spectrograms to detect anomalous vibration patterns. This output feeds into the main unsupervised anomaly detection models.

**In plain terms:** The vibration sensor's raw output isn't useful on its own — it gets converted into an image-like format (a spectrogram) and fed into its own small model that learns what normal vibration looks like, so it can flag unusual shaking as a separate signal that feeds into Phase 8\.

- [ ] 🔴 **🤖 Generate vibration spectrogram dataset**  
  *→ Converts raw MPU6050 vibration readings from all visits into the spectrogram images the convolutional model needs — required before any CNN training can begin.*  
     
     
  \- Per trial: MPU6050 100 Hz × 60s \\= 6,000 samples → FFT spectrogram image.    
     
  \- \\\~240 spectrograms per unit over 6 months (24 visits × 10 trials). 35 units × 240 ≈ 8,400 spectrograms total.    
     
  \- Organize: train on normal-condition units (majority), validate on known-fault \\+ injected-fault units.  
     
- [ ] 🔴 **🤖 Train convolutional autoencoder**  
  *→ Trains the vibration-specific model to learn what normal vibration spectrograms look like, so it can later flag ones that don't fit — this output feeds into the main models in Phase 8\.*  
     
     
  \- Architecture: MobileNetV2 encoder (pretrained ImageNet weights) → latent bottleneck → decoder.    
     
  \- Loss: MSE reconstruction error.    
     
  \- Save best model (lowest val\\\_loss) as \`cnn\_vibration\_autoencoder.pth\`.    
     
  \- Output per spectrogram: reconstruction error (anomaly score) \\+ latent feature vector.  
     
- [ ] 🟠 **🤖 Vibration anomaly detection evaluation** *(feeds H1b)*  
  *→ Checks whether the trained vibration model actually catches known or injected faults — the direct evidence for hypothesis H1b, whether vibration data meaningfully helps detection.*  
     
     
  \- Test on injected-fault units: reconstruction error must increase significantly post-fault vs. pre-fault.    
     
  \- Test on known-fault units from maintenance logs: reconstruction error should be higher than fleet average.    
     
  \- Report: true positive rate on injected faults, anomaly score separation (Mann-Whitney U).  
     
  \- Output ready for Phase 8 H1b ablation: CNN reconstruction error \+ latent vector extracted per trial.  
     
- [ ] 🟡 **🤖 Ablation study** (if time permits)  
  *→ An optional deeper test, removing pieces of the vibration model or its inputs one at a time to see which parts are actually doing the work — useful for the discussion chapter if time allows.*  
     
     
  \- Compare: pretrained MobileNetV2 encoder vs. custom CNN from scratch.    
     
  \- Compare: reconstruction error vs. latent feature vector as anomaly score.    
     
  \- Compare: spectrogram resolution (frequency bins, time windows).

### Nested Paper Tasks

- [ ] 🟠 **📝 Write Chapter 4 vibration CNN results**  
  *→ Documents how well the vibration model performed, feeding directly into the H1b results write-up in the main anomaly-detection findings chapter.*  
     
  \- Report: architecture, dataset size, training curves (loss over epochs), anomaly score distributions.  
  \- Include: sample spectrograms (normal vs. anomalous with reconstruction overlay), anomaly score distributions for known-fault vs. healthy units.

---

## Phase 8 — Machine Learning: Unsupervised Anomaly Detection

**Goal:** Train and evaluate the 4 unsupervised models on full sensor \+ vibration feature set. Compare performance. Run the conditional supervised secondary experiment if fault injection yields enough labeled data.

**In plain terms:** This is the core "does it work" phase — training the four anomaly-detection models on the collected data (including the vibration signal from Phase 7), then running every planned test to see which model, if any, reliably tells healthy units from degraded ones.

### Preprocessing Pipeline

*What this covers: turning raw calibrated sensor readings into the exact feature set the models expect — scaling values, reducing dimensions, and merging in the vibration signal from Phase 7\.*

- [ ] 🔴 **🤖 Complete preprocessing pipeline**  
  *→ Builds the final pipeline that turns calibrated data into whatever exact feature format each of the four models needs, including fitting PCA only on known-normal data so it doesn't "see" anomalies during training.*  
     
     
  \- Implementation in \`03\_Code/2\_preprocessing/\`.    
     
  \- Features: set\\\_temp \\+ 8 calibrated sensor readings \\+ vibration anomaly score from CNN \\+ vibration statistical features (RMS, kurtosis, peak frequency) \\+ time-since-last-cleaning.    
     
  \- Standardization: fit on normal-condition units only, transform all data.    
     
  \- PCA: fit on normal-condition units; plot variance explained; select k with ≥ 95% cumulative variance.    
     
  \- Output: X\\\_all, metadata (unit\\\_id, timestamp, kit\\\_id, location) saved to \`02\_Data/processed/\`.  
     
- [ ] 🟠 **🤖 Feature importance analysis**  
  *→ Identifies which sensor features are actually driving the models' anomaly scores — the direct evidence for RQ1/H1a about which measurements matter most.*  
     
     
  \- Univariate Mann-Whitney U: which features differentiate known-fault from known-healthy units.    
     
  \- Permutation importance (using Isolation Forest as reference model).    
     
  \- Report: top 5 most discriminative features, effect sizes, p-values.

### Model Training

*What this covers: actually fitting the four anomaly-detection models to the collected data, using the settings and search space defined back in Phase 5\.*

- [ ] 🔴 **🤖 Train Isolation Forest**  
  *→ Fits the first of the four primary models to the processed data — each is trained and evaluated somewhat independently so they can be fairly compared afterward.*  
     
     
  \- Hyperparameter tuning via grid search (contamination, n\\\_estimators, max\\\_samples).    
     
  \- Save \`isolation\_forest.pkl\`.    
     
  \- Feature importance: which features drive isolation.  
     
- [ ] 🔴 **🤖 Train One-Class SVM**  
  *→ Fits the second primary model, which draws a boundary around what "normal" looks like rather than isolating points like Isolation Forest — different models catch different kinds of anomalies.*  
     
     
  \- Hyperparameter tuning via grid search (nu, gamma, kernel).    
     
  \- Scale features before training (SVM is distance-sensitive).    
     
  \- Save \`one\_class\_svm.pkl\`.  
     
- [ ] 🔴 **🤖 Train Gaussian Mixture Model**  
  *→ Fits the third primary model, which scores anomalies based on how (un)likely a reading is under a learned probability distribution of normal behavior.*  
     
     
  \- Select n\\\_components via BIC (test 1-10 components).    
     
  \- Save \`gmm.pkl\`.    
     
  \- Report: per-component means (interpretable "normal operating modes").  
     
- [ ] 🔴 **🤖 Train Autoencoder**  
  *→ Fits the fourth primary model, which flags anomalies by how badly it fails to reconstruct a reading — often the most sensitive of the four, but also the most complex to tune.*  
     
     
  \- PyTorch implementation.    
     
  \- Architecture per Phase 5 definition.    
     
  \- Early stopping (patience=10 on validation reconstruction loss).    
     
  \- Save \`autoencoder.pth\`.

### Model Evaluation

*What this covers: running every planned statistical test against the trained models to check whether the hypotheses from Phase 1 hold up — the section that answers "did it actually work?"*

- [ ] 🔴 **🤖 Layer 1 — Retrospective log validation** *(H1a \+ H2a-MW)*  
  *→ Runs the first validation layer: comparing anomaly scores on the 13 known-fault units against the healthy fleet — this directly produces the H1a and H2a-MW results.*  
     
     
  \- Deploy kit to known-fault units (1-2 visits each).    
     
  \- \*\*H1a:\*\* Anomaly score separation per sensor measurement group (supply-return temp differential, compressor/fan current signatures, vibration spectral features) between known-fault and known-healthy units. Mann-Whitney U, p \\\< 0.05.  
     
  \- \*\*H2a-MW:\*\* All 4 models tested for anomaly score separation between known-fault and known-healthy units. Mann-Whitney U, p \\\< 0.05.  
     
  \- Report: mean anomaly score per group, effect size (Cohen's d).  
     
- [ ] 🔴 **🤖 H2b — PCA parity test**  
  *→ Checks whether using the PCA-compressed feature set loses meaningful performance compared to the full feature set — if not, it justifies using the simpler, smaller feature set going forward.*  
     
     
  \- Train best model on full features and on PCA-reduced features (k components with ≥ 95% cumulative variance).    
     
  \- Compare: \|TPR\_full − TPR\_PCA\| ≤ 3 percentage points.    
     
  \- McNemar's test on binary classification outcomes (above/below threshold): p \\\> 0.05 → no significant difference → PCA is viable.    
     
- [ ] 🟠 **🤖 H1b — Vibration ablation (paired bootstrap)**  
  *→ Statistically tests whether including the vibration signal actually improves results over temperature-and-electrical data alone, using the paired bootstrap test specified back in Phase 1\.*  
     
     
  \- Requires Phase 7 vibration features (CNN reconstruction error \+ latent vector, or statistical: RMS, kurtosis, peak frequency).    
     
  \- Train two model variants of the best model: temperature+electrical only vs. temperature+electrical+vibration. Same hyperparameters.    
     
  \- Compute performance metric (AUC or TPR) on held-out validation set for both variants.    
     
  \- Paired bootstrap (1,000+ resamples): compute performance gap per resample. If 95%+ of gaps \\\> 0 → p \\\< 0.05 → vibration contributes significantly.    
     
- [ ] 🔴 **🤖 Layer 2 — Controlled fault injection validation** *(H2a-TPR)*  
  *→ Runs the second validation layer: checking that anomaly scores actually rose after the deliberately-injected faults from Phase 6, producing the true-positive-rate evidence for H2a.*  
     
     
  \- Run all 4 models on pre-fault → post-fault → recovery data.    
     
  \- \*\*H2a-TPR:\*\* Anomaly score must rise post-injection for each fault type. True positive rate ≥ 80% across injected faults.    
     
  \- False positive rate on known-healthy fleet ≤ 15%.  
     
- [ ] 🔴 **🤖 Layer 4 — Confound verification** *(H4b)*  
  *→ Checks that the anomaly score isn't secretly just responding to weather, time-since-cleaning, or which physical kit was used — this produces the H4b results and rules out hidden bias.*  
     
     
  \- Assemble per-unit metadata: anomaly score, time-since-last-cleaning, ambient temp, ambient humidity, kit ID, location.    
     
  \- \*\*Spearman's ρ:\*\* anomaly score vs. days-since-cleaning, ambient temp, ambient humidity. All p \\\> 0.05 → no correlation.    
     
  \- \*\*ANOVA:\*\* anomaly score across kit IDs and locations. p \\\> 0.05 → no kit/location bias.    
     
  \- If any confound correlates → include it as a model feature, retrain, report both (with and without).  
     
- [ ] 🟠 **🤖 Layer 3 — Technician agreement**  
  *→ Compares the model's anomaly rankings against the independent technician spot-check opinions from Phase 6, adding a human-judgment cross-check to the statistical validation layers.*  
     
     
  \- Monthly spot-check findings vs. anomaly scores.    
     
  \- Report: agreement rate, Cohen's Kappa.  
     
- [ ] 🟠 **🤖 Layer 5 — Maintenance reset**  
  *→ Checks that anomaly scores actually drop after a flagged unit gets cleaned — if the score doesn't respond to an intervention known to help, that undermines confidence in what it's measuring.*  
     
     
  \- For units cleaned mid-study: anomaly score pre-cleaning vs. post-cleaning.    
     
  \- Expect: significant drop post-cleaning.    
     
  \- Report: paired t-test or Wilcoxon signed-rank.  
     
- [ ] 🟠 **🤖 Model comparison** *(answers H2a — which model wins?)*  
  *→ Puts all four models' results side by side to answer H2a directly: which one, if any, is the best performer overall.*  
     
     
  \- Comparison table: Isolation Forest vs. One-Class SVM vs. GMM vs. Autoencoder.    
     
  \- Metrics: TPR on injected faults, FPR on healthy fleet, anomaly score separation (effect size), agreement with technician.    
     
  \- Ranking: which model performs best overall? Report per H2a: at least one must achieve p\<0.05 (Mann-Whitney) AND TPR ≥80%.  
     
- [ ] 🟠 **🤖 H4a — Unit-level generalization (Leave-One-Unit-Out)**  
  *→ Tests the winning model on AC units it never saw during training, to confirm it learned general fault patterns rather than memorizing the specific 30-40 units in the study.*  
     
     
  \- LOUO evaluation: for each unit U, train on all other units, score U. Repeat for all units.    
     
  \- Compare TPR (or AUC) on held-out units vs. in-sample units: \|performance gap\| ≤ 5 percentage points.    
     
  \- McNemar's test comparing in-sample vs. held-out binary outcomes: p \\\> 0.05 → no significant difference → model generalizes.    
     
  \- Report: does performance degrade significantly vs. random split? If yes → model is learning unit identities, not fault signatures.  
     
- [ ] 🟡 **🤖 H3 (conditional) — PMV composite metric comparison**  
  *→ Only runs if the DIY airflow sensor actually worked — compares using a single combined comfort score against using raw temperature/humidity/airflow separately.*  
     
     
  \- Requires: DIY airflow sensor built and functional. If sensor fails → H3 and RQ3 silently dropped.    
     
  \- Compute PMV per trial (temp, humidity, airflow, radiant temp).    
     
  \- Train model on PMV-only features vs. raw environmental features. Best model from comparison.    
     
  \- Compare TPR/AUC: \|performance\_gap\| ≤ 3 percentage points → PMV is a viable alternative.  

### Conditional Secondary: Supervised Classification

*What this covers: an optional bonus experiment that only runs if fault injection produced enough labeled faulty examples to make a supervised model meaningful.*

- [ ] 🟡 **🤖 IF fault injection yields ≥ 30 labeled samples**  
  *→ The trigger condition for the optional secondary experiment — only if enough labeled faulty examples exist does it make sense to also try a supervised model as a bonus comparison.*  
     
  \- Train: RF, XGBoost, RBF SVM on labeled subset (fault-injected \+ known-fault \+ known-healthy).  
  \- Split: Group K-Fold by unit ID (all readings from one unit in same fold).  
  \- Report: macro-F1, per-class precision/recall, confusion matrix.  
  \- Compare: does supervised classification with labels outperform unsupervised anomaly detection? If yes → strong evidence for labeled-data value. If no → unsupervised is genuinely better for this problem.  
  \- **Do NOT** run if \< 30 labeled samples; this experiment is conditional and its absence is documented.

### Nested Paper Tasks

- [ ] 🟠 **📝 Write Chapter 4 anomaly detection results**  
  *→ Pulls together every model's performance and every hypothesis test from this phase into the results chapter — the single biggest results section in the whole thesis.*  
     
  \- Per hypothesis: statistical test results, effect sizes, p-values (H1a, H1b, H2a, H2b, H3-if-conditional, H4a, H4b).  
  \- Per layer: validation results table summarizing which hypotheses were tested by which layer.  
  \- Model comparison table with all metrics.  
  \- Confound verification: Spearman's ρ results, ANOVA results.  
  \- Feature importance: top discriminative sensor readings.  
  \- Interpretation: which model is recommended and why.

---

## Phase 9 — Deployment

**Goal:** Build the Streamlit dashboard and automated anomaly scoring pipeline. Deploy on the Ingest Server for live use during the final month of the study.

**In plain terms:** Once a model is trained and validated, this phase wires it up so it runs automatically — new readings come in, get scored for anomalies, and show up on a live dashboard that maintenance staff could actually look at.

> **Note:** Current deployment (thesis) uses a single ingest server with manual weekly data collection via portable kits. The long-term vision (Campus of the Future) is a permanently-installed sensor module per AC unit streaming continuously to a centralized server.

### Server Setup

- [ ] 🔴 **🚀 Ingest Server configuration**  
  *→ Sets up the machine that will receive incoming sensor data and run the live scoring pipeline — the foundation the rest of Phase 9 is built on.*  
     
     
  \- Set up dedicated PC or laptop with Python environment.    
     
  \- Configure Wi-Fi network (same as Master ESP32).    
     
  \- Install: Python 3.11+, watchdog, streamlit, joblib, pandas, numpy, scikit-learn, pytorch, sqlite3.    
     
  \- Set up directory structure from DMP.  
     
- [ ] 🔴 **💻 Ingest service script**  
  *→ The always-running program that actually receives new data as it comes in from the field and hands it off to the rest of the pipeline.*  
     
     
  \- Reads Serial from Master ESP32.    
     
  \- Validates and writes to \`02\_Data/raw/\`.    
     
  \- Runs as persistent background process.

### Anomaly Scoring Pipeline

*What this covers: the automated code that takes a new incoming reading, processes it the same way training data was handled, runs it through the trained model, and decides whether to raise an alert.*

- [ ] 🔴 **🚀 Watchdog automation setup**  
  *→ Configures a file-watching process that automatically triggers scoring the moment a new data file arrives, instead of requiring someone to manually run the pipeline after every visit.*  
     
     
  \- Monitor \`02\_Data/raw/\` for new files (use staging directory \\+ atomic move to prevent race conditions).    
     
  \- Trigger on new complete CSV → load → apply CCFs → preprocess → load best model → compute anomaly score → store result.  
     
- [ ] 🔴 **💻 Automated anomaly scoring script**  
  *→ Takes a new reading, runs it through the trained model from Phase 8, and produces an anomaly score — this is what makes the system "live" rather than something researchers re-run by hand.*  
     
     
  \- Load best model (e.g., \`isolation\_forest.pkl\`).    
     
  \- Load scaler \\+ PCA transformer (fit during Phase 8).    
     
  \- Process: set\\\_temp \\+ 8 sensor readings → calibrated → standardized → PCA → model.anomaly\\\_score().    
     
  \- Store: \`{unit\_id, timestamp, anomaly\_score, sensor\_snapshot}\` → \`anomalies.db\`.    
     
  \- Error handling: catch NaN, malformed input, shape mismatch → log error → skip file.  
     
- [ ] 🟠 **🚀 SQLite anomalies database**  
  *→ Stores every anomaly score and alert in a simple local database so the dashboard has something to query and there's a historical record, not just a number that disappears after each run.*  
     
     
  \- Schema: \`anomalies\` table (id, unit\\\_id, timestamp, anomaly\\\_score, model\\\_name, sensor\\\_json).    
     
  \- Schema: \`alerts\` table (id, unit\\\_id, timestamp, severity, anomaly\\\_score\\\_threshold\\\_exceeded, acknowledged).    
     
  \- Create indexes on unit\\\_id, timestamp for query performance.  
     
- [ ] 🟡 **💻 Alert threshold logic**  
  *→ Decides at what anomaly score a unit should actually get flagged for attention — without this, every unit just has a raw number with no clear "needs attention" signal.*  
     
     
  \- Anomaly score in top 5% of training distribution → warning.    
     
  \- Anomaly score in top 1% → alert.    
     
  \- 3 consecutive alerts for same unit → critical (flag for immediate inspection).    
     
  \- Configurable via \`config.yaml\`.

### Dashboard

- [ ] 🟠 **🚀 Streamlit dashboard — main status page**  
  *→ The at-a-glance view — likely a grid of all monitored units color-coded by status — meant to be the first thing someone checks to see overall fleet health.*  
     
     
  \- \`app.py\` with overview: all 30-40 units, most recent anomaly score each.    
     
  \- Color-coded grid: 🟢 Normal (below 95th percentile) / 🟠 Warning (95-99th) / 🔴 Alert (above 99th).    
     
  \- Auto-refresh every 30 seconds or triggered by watchdog file event.  
     
- [ ] 🟠 **🚀 Streamlit dashboard — unit detail page**  
  *→ A drill-down view for a single unit, showing its sensor history and score trend over time, for when the main status page flags something worth investigating.*  
     
     
  \- Dropdown: select unit by ID.    
     
  \- Historical chart: sensor time-series (temp, current, voltage) \\+ anomaly score overlay.    
     
  \- Anomaly history: date → anomaly score → alert status.    
     
  \- Time-since-last-cleaning indicator.  
     
- [ ] 🟡 **🚀 Streamlit dashboard — admin page**  
  *→ A back-end view for managing the system itself (units, kits, thresholds) rather than for day-to-day monitoring.*  
     
     
  \- Model retraining trigger button.    
     
  \- Data collection status (units not visited this week).    
     
  \- Alert acknowledgment UI.  
     
- [ ] 🟡 **💻 Streamlit authentication** (optional)  
  *→ An optional login layer, since a dashboard showing facility data probably shouldn't be open to anyone who finds the link.*  
     
     
  \- Simple password protection via environment variable or config.    
     
  \- Read-only view for maintenance staff, admin view for researchers.

### Cloud Sync (Optional)

- [ ] 🟢 **🚀 Supabase cloud backup**  
  *→ An optional nightly copy of the data to the cloud, purely as a safety net in case the local server or database is lost — not required for the core system to function.*  
     
  \- Nightly sync script: `anomalies.db` → Supabase.  
  \- Ensure API key is NOT stored in plaintext (use environment variable).

### Nested Paper Tasks

- [ ] 🟠 **📝 Finalize Chapter 3 deployment section**  
  *→ Documents the deployment architecture actually built in this phase, so the methodology chapter reflects the real implementation rather than the original plan.*  
     
  \- Replace theoretical deployment plan with implementation summary.  
  \- Include: architecture diagram, technology choices, deployment workflow.  
  \- Add dashboard screenshots in Appendix.

---

## Phase 10 — Finalization

**Goal:** Complete all writing, integrate results, format for submission, and prepare defense.

**In plain terms:** This is assembling everything already built and tested into the final written thesis — results, discussion, conclusions, and the slides for defending it.

### Chapter 4 — Complete Results & Discussion

- [ ] 🔴 **📝 Integrate all Chapter 4 subsections**  
  *→ Chapter 4 gets written piecemeal across Phases 4, 7, 8, and 9 (calibration, vibration, anomaly detection, deployment results) — this pulls them into one coherent, consistently-formatted chapter.*  
     
     
  \- 4.1 Sensor calibration (BME280, DS18B20, ACS712, ZMPT101B).    
     
  \- 4.2 Vibration CNN spectrogram anomaly detection results.    
     
  \- 4.3 Dataset overview (feature statistics, PCA results, unit-level distributions, time-since-cleaning profiles).    
     
  \- 4.4 Unsupervised anomaly detection results — all 4 models.    
     
  \- 4.5 Validation layer results (retrospective logs, fault injection, technician agreement, confound checks, maintenance reset).    
     
  \- 4.6 Conditional supervised classification results (if applicable).    
     
  \- 4.7 Deployment results (dashboard screenshots, anomaly scoring latency, system uptime).  
     
- [ ] 🔴 **📝 Discussion per section**  
  *→ Adds the "so what does this mean" interpretation after each results subsection — raw numbers alone don't tell a reader whether a result is good, expected, or concerning.*  
     
     
  \- Why did model X outperform model Y? Link back to literature.    
     
  \- Were the hypotheses supported? (H1a–H4b: 7 hypotheses, each with statistical test results).    
     
  \- How did the 4-layer validation strategy perform — which layers provided strongest evidence?    
     
  \- Limitations encountered (sensor noise, dataset size, sparse known-fault units, ambient confounds).    
     
  \- Implications for Xavier University maintenance practices and Campus of the Future.

### Chapter 5 — Conclusion & Recommendations

- [ ] 🟠 **📝 Write conclusions**  
  *→ Directly answers each of the four RQs from Chapter 1 based on what was actually found, closing the loop the paper opened at the very start.*  
     
     
  \- Summary of what was built and tested.    
     
  \- Answer each research question directly.    
     
  \- Key finding: which model is recommended and why.  
     
- [ ] 🟠 **📝 Write recommendations**  
  *→ Translates the findings into concrete next steps — for PPO's actual use of the system, or for the Campus of the Future rollout — rather than leaving the thesis as a purely academic exercise.*  
     
     
  \- For Xavier University PPO: adopt anomaly detection as triage tool, integrate with existing quarterly maintenance cycle. Transition from portable proof-of-concept to permanent per-unit sensor modules (weatherproof enclosure, AC-powered, fixed mounting brackets, automated calibration, remote firmware updates).    
     
  \- For future research: multi-fault type classification, permanent sensor installation, regression-based degradation forecasting, mobile app, expansion to all 2,599 campus units.    
     
  \- For hardware: external ADC for ACS712, permanent mounting brackets, automated calibration protocol.

### Final Deliverables

- [ ] 🟠 **📝 Abstract** — 250-300 words.  
  *→ The short summary that's often the only part many readers ever see — written last because it has to accurately summarize a completed thesis, not a planned one.*  
     
- [ ] 🟡 **📝 Acknowledgements**.  
  *→ The standard thank-you section — for advisers, PPO staff, and anyone else who supported the study.*  
     
- [ ] 🟡 **📝 Appendices** — calibration data tables, R regression outputs, full code listings, dashboard screenshots, maintenance log excerpts, fault injection protocols.  
  *→ Houses supporting material too detailed for the main chapters (raw calibration tables, full code listings, maintenance log excerpts) but still needed for someone verifying the work.*  
     
- [ ] 🟡 **📋 APA/citation audit** — check all in-text citations → reference list, consistent format throughout.  
  *→ A final pass checking every in-text citation has a matching reference-list entry and vice versa — a common, easily-avoidable source of point deductions.*  
     
- [ ] 🟡 **📋 Table of Contents, List of Figures, List of Tables** — auto-generated.  
  *→ Auto-generated once the document structure is finalized — doing this too early just means redoing it after every edit.*  
     
- [ ] 🟡 **📋 Defense presentation** — 15-20 slides.  
  *→ The slide version of the whole thesis, built last since it should reflect the final, defended version of the results rather than an earlier draft.*  
     
  \- Problem & motivation: the information gap between cleanings.  
  \- Architecture: non-invasive → 2 portable kits → ESP-NOW → anomaly detection (proof-of-concept for permanent per-unit modules on Campus of the Future).  
  \- Methodology: why unsupervised? (walk through the 13-in-2,599 math).  
  \- Key results (1 slide per major finding).  
  \- Validation: the 4-layer evidence.  
  \- Conclusions & recommendations.  
  \- Demo video of dashboard (1-2 min).

---

## Milestones & Deadlines

*Dates below are still placeholders (`YYYY-MM-DD`) — fill these in once the group agrees on a schedule; the Milestone/Deliverables columns describe what "done" looks like for each phase.*

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

