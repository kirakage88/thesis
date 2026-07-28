# Methodology Recommendation: Supervised vs Unsupervised

## 1. Recommendation: Option B (Unsupervised Anomaly Detection)

The deciding factor is arithmetic, not theory.

You have 30–40 monitored units. Across the entire campus (2,599 units), only 13 have documented issues — and there is **no guarantee any of those 13 are in your study sample.** Even with weekly technician inspections, your study population is overwhelmingly healthy. Realistically you are looking at **0–3 naturally occurring Abnormal observations** over 6 months, out of ~180–400 total unit-visits.

Supervised binary classification needs to learn a decision boundary between two classes. With fewer than ~10 positive-class instances on a 30-feature space, every algorithm in Option A's lineup collapses to one of two outcomes:

- **Overfit** to the handful of abnormal examples (memorizing them, failing to generalize).
- **Collapse to majority class** (predict Normal for everything, achieve 90%+ accuracy, 0% recall on the class that actually matters).

Neither outcome produces a usable model or a defensible thesis result. The labeling bottleneck isn't just cost — it's that you physically cannot manufacture enough Abnormal labels in 6 months at this scale without deliberate fault injection, which the supervised framework doesn't propose.

Unsupervised anomaly detection sidesteps this entirely. It trains on the abundant Normal data (which is ~95%+ of your data), learns the operating envelope, and flags deviations. This is exactly what a triage tool should do: "this unit looks different from the fleet — investigate." It doesn't promise to diagnose; it promises to prioritize.

The alignment with the complementary-triage framing is also cleaner. A supervised classifier that says "Abnormal" implicitly demands ground truth — and you don't have it. An anomaly detector that says "score 0.82, outside 95th percentile of fleet baseline" is honest about its epistemic limits.

**Concrete recommendation:** Isolation Forest as the primary model (handles mixed feature types, non-parametric, well-suited to small-medium data, established in anomaly detection literature), with One-Class SVM as a comparison baseline. Autoencoder is an option if you want the CNN-spectrogram branch, but good luck defending AE training with 200 samples in a thesis defense.

---

## 2. Strongest Argument FOR Option A (the one not chosen)

The cleanest metric story and the strongest literature precedent.

"F1 = 0.87, precision = 0.91, recall = 0.83" is instantly comprehensible to any thesis panel member, any maintenance manager, and any future employer. The question "does this model correctly classify units as Normal or Abnormal?" is the question every stakeholder wants answered. It produces a binary, actionable output. The HVAC PdM literature is overwhelmingly supervised classification — claiming alignment with existing research is straightforward, and a panel member can easily find 5–10 comparable papers to benchmark against.

Anomaly detection, by contrast, forces the panel to accept an unfamiliar evaluation paradigm. "The model flagged 7 of 13 known-fault units retrospectively, with a false positive rate of 12%" is a harder sell than "F1 = 0.85." Supervised classification is also what the adviser likely expected when they approved the original proposal — switching to unsupervised means managing that expectation.

---

## 3. Validation Strategy for Option B

This is the crux. Without a strong validation story, the defense fails. A layered approach:

### Layer 1 — Retrospective log validation (existing data)

Deploy the sensor kit briefly (1–2 visits) to the **13 known-fault units** from maintenance logs that are outside the main study sample but on the same campus. If the anomaly model flags these as high-anomaly with significantly higher scores than the known-healthy fleet, that's your first validation signal. This is your closest analog to a labeled test set.

Metric: **separation** — does the anomaly score distribution for the 13 known-fault units differ significantly from the study fleet (Mann-Whitney U test, p < 0.05)? If yes, the model is picking up fault signatures, not noise.

### Layer 2 — Controlled fault injection (strongest single validation)

With campus facilities' permission, **deliberately induce known faults** on 2–3 units during a maintenance window:

- Partially block the return air grille (simulating fouling/obstruction)
- Reduce refrigerant charge via the service valve (simulating a leak — requires a licensed technician, but this is a one-time supervised procedure, not ongoing)
- Misalign the fan blade (simulating mechanical imbalance)

Record baseline → induce fault → record post-fault sensor data. The anomaly model should show a significant score increase post-injection. This is the **gold standard** validation: you know ground truth because you created it. It's analogous to stress-testing a structural model — standard engineering methodology.

Report: true positive rate on injected faults, magnitude of anomaly score shift, and which sensor features drove the detection.

### Layer 3 — Prospective technician spot-checks

On a rotating subset of 5–8 units per month, a technician does a brief visual inspection (the invasive labeling pass from my earlier review). Correlate technician findings with anomaly scores. Units flagged by both the model and the technician = true positives. Units flagged by model but not technician = investigate (sensor error, ambient confound, or model false positive). Units flagged by technician but not model = missed faults.

This is small-scale, but it adds **qualitative validation** that the anomalies the model surfaces are operationally meaningful, not just statistical artifacts.

### Layer 4 — Confound verification

Run the anomaly score against:

- **Time-since-cleaning:** if anomaly score monotonically increases with time-since-last-cleaning, the model may just be detecting dust accumulation, not faults. This is actually useful (dust-driven performance degradation *is* the signal), but it should be characterized, not discovered in defense.
- **Ambient temperature/humidity:** if anomaly score spikes on hot days across all units simultaneously, the model is detecting weather, not faults. Include ambient conditions as covariates or normalize features by ambient readings.
- **Kit ID:** verify the two portable kits don't produce systematically different anomaly scores (calibration confound).

Report all three as **confound checks**, not failures. If the model passes them, the defense argument is: "We tested whether the model was detecting faults vs. detecting weather / dust / sensor-drift, and it is detecting faults."

### Evaluation metrics summary for Option B

| Metric | Source | Target |
|---|---|---|
| Anomaly score separation (fault vs. healthy) | Mann-Whitney U on Layer 1 + Layer 2 | p < 0.05 |
| True positive rate on injected faults | Layer 2 | ≥ 80% |
| False positive rate on known-healthy fleet | Layer 1 + study fleet | ≤ 15% |
| Anomaly score not confounded by weather/kit/time-since-cleaning | Layer 4 | No significant correlation (p > 0.05) |
| Technician agreement (qualitative) | Layer 3 | ≥ 70% agreement on flagged units |

These are all falsifiable, all testable with the study's resources, and address the concern.

---

## 4. If You Went With Option A: Addressing Labeling and Imbalance

**Labeling bottleneck:** Controlled fault injection (same as Layer 2 above) is the only way to generate enough positive-class samples in 6 months. Induce faults on 5–10 units per month (rotating), with each fault type repeated across multiple units. This produces ~30–60 artificially-generated Abnormal observations alongside the 0–3 natural ones. A technician labels each visit as Normal/Degraded during the weekly visit (this is the invasive inspection that the proposal implies but doesn't explicitly plan).

This is defensible because the *deployed* system is non-invasive — the fault injection is **part of the experimental design**, not part of the operational system. A bachelor's thesis can deliberately create faults for training and test whether the sensors detect them.

**Addressing imbalance:** SMOTE or ADASYN oversampling on the minority class, plus class-weight adjustment in RF/XGBoost. Report macro-F1 (not accuracy — accuracy will be meaningless at 95:5 imbalance). Stratified k-fold cross-validation. Expect recall on the Abnormal class to be the binding constraint — optimize for recall, accept lower precision.

**Honest limit:** Even with fault injection, ~50–70 total positive examples is the minimum floor viable for supervised learning on RF/XGBoost. SVM and k-NN can work at this scale; DNN cannot. Drop the DNN from the lineup.

---

## 5. Which Option Is Easier to DEFEND

**Option A — supervised classification — is easier to defend** in a traditional Mechanical Engineering thesis defense, regardless of which is technically better for this problem.

Reasons that have nothing to do with methodology quality:

- Panel members are more likely to recognize "F1 = 0.87" than "anomaly score separation p < 0.05." Familiarity reduces the cognitive barrier to passing the work.
- The phrase "supervised ML classification" is expected for a thesis titled "Predictive Maintenance Model." Switching to unsupervised anomaly detection requires re-educating the panel on why you deviated from the standard approach — a non-trivial defense burden.
- The question "what is your model's accuracy?" has a clean answer in supervised. "We don't use accuracy, we use anomaly score separation" is technically correct but harder to defend against a panelist who keeps asking for it.
- Literature precedent: a panel member who checks the HVAC PdM literature will find supervised classification papers everywhere. Unsupervised will require justification for the deviation.

**However:** Option A is only easier to defend **if it produces results.** If the supervised model collapses to majority-class prediction (which is likely given the data constraints), the defense becomes "my model predicts Normal for everything, which is 92% accurate" — which is worse than defensible, it's a failed thesis.

---

## Practical Recommendation: Hybrid Approach

Given the constraints, the most defensible architecture is:

**Primary investigation (Option B):** Unsupervised anomaly detection as the main methodological contribution, with Isolation Forest and One-Class SVM as primary models, validated through retrospective log comparison (13 known-fault units), fault injection, and technician spot-checks.

**Secondary investigation (hybrid):** If fault injection produces enough labeled abnormal samples (30+), run supervised classifiers **as a comparison experiment** — demonstrating whether supervised outperforms unsupervised when labels are available. This gives the panel their familiar metrics while the primary contribution rests on the more honest unsupervised method.

This framing lets you say in defense: "The primary method is unsupervised anomaly detection because labeled fault data is scarce. As a secondary experiment, we tested whether supervised classification could improve performance when a labeled subset was constructed via fault injection, and found [X]."

This is both defensible and honest. The supervised arm is a bonus, not a dependency. If fault injection doesn't produce enough samples, the unsupervised arm stands alone. If the supervised arm fails, you have the unsupervised results. If the supervised arm succeeds, you have a richer thesis.