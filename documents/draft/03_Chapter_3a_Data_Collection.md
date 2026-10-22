# Chapter III (Part 1): Data Collection

> **Working draft (2026-10-21):** This file currently contains only the updated **3.1.3 Sampling Plan**. Insert it after 3.1.2 Sources of Data. Table numbers are provisional. The rest of Chapter 3a still lives in `documents/original/03_Chapter_3a_Data_Collection.md` and must be reconciled with the current scope and planned hardware (35 healthy + 2 injected units ideal; 20 healthy + 2 injected minimum; current/power/airflow/vibration, no ESP32-CAM; six visits per unit ideal, three minimum).

### 3.1.3 Sampling Plan

**Purposive sampling** will be used to select **35 healthy split-type air conditioning units plus 2 injected units (37 total)** for the ideal scenario, and **20 healthy units plus 2 injected units (22 total)** for the minimum scenario. The healthy units come from the SBM AVR Facilities, College of Engineering, and Faber Hall. The 2 injected units are separate from the healthy units and are never used for training. Units with documented maintenance concerns will be prioritized for supporting retrospective comparisons, while only normal-condition units will supply training data.

#### Definitions

| Term | Definition |
|---|---|
| **Unit** | One split-type AC unit (the physical machine). |
| **N_healthy** | Number of healthy units used for training. |
| **N_injected** | Number of units that receive controlled fault injection; fixed at 2. |
| **N_total** | Total number of units: N_healthy + N_injected. |
| **Healthy unit** | A normal-condition unit used only for normal operation. Supplies the model's training data. |
| **Injected unit** | A unit that receives controlled fault injection. Never used for training. |
| **Visit (V)** | One trip where a sensor kit is placed on one healthy unit. V = visits per healthy unit. |
| **Trial (T)** | One continuous 1-minute recording. Healthy visits have T = 10 trials; injected phases have T_phase = 8–10 trials per phase. |
| **Sample** | One raw sensor reading at one instant (10 Hz: ambient/current/airflow; 100 Hz: vibration). One trial = 600 samples at 10 Hz, 6,000 at 100 Hz. |
| **Window (w, s, W)** | A fixed-length slice of a trial. Features are computed per window, giving one feature vector. w = window length; s = stride; W = floor((L − w)/s) + 1, where L = 60 s. |
| **Feature vector** | The numbers computed from one window (e.g., mean temperature, RMS current, vibration RMS, kurtosis, peak frequency). |
| **Spectrogram** | A time-frequency representation of one 10-s vibration window, used as input to the CNN autoencoder. |
| **Anomaly score** | The model's output for a window (higher = more abnormal). |
| **Trial score** | One anomaly score per trial: the median of that trial's window scores. This is the value used in statistical tests. |
| **Pair** | A pre-injection trial matched with a post-injection trial under similar conditions (time of day, setpoint, ambient). |
| **Pseudoreplication** | Treating non-independent data as independent (e.g., counting 600 readings from one minute as 600 separate samples), which inflates significance. |

#### Core rule: windows are not the sample size for testing

- Windows from the same trial are correlated because they are adjacent slices of the same recording.
- Windows are used to train the models and to build a stable score.
- Trials are the independent data points used in hypothesis tests (one trial score = one point).
- Statistical tests are never run directly on windows.

#### Window settings

| Setting | Value |
|---|---|
| Trial length (L) | 60 s |
| Window length (w) | 10 s |
| Stride (s) | 10 s (no overlap) → W = (60 − 10)/10 + 1 = **6 windows/trial** |

This study uses only the no-overlap setting: every trial yields exactly **6 windows**. At 100 Hz, a 10-s vibration window contains 1,000 samples, giving 0.1 Hz frequency resolution up to 50 Hz.

#### Data volume

- Windows per healthy unit = V × T × W
- Healthy windows = N_healthy × V × T × W
- Injection windows = N_injected × 3 faults × 3 phases × T_phase × W
- Total windows = healthy windows + injection windows
- Training windows = healthy windows from normal-condition units only

**Table 3.1. Ideal sampling scenario (35 healthy + 2 injected units; V = 6; T = 10; W = 6).**

| Group | Units | Windows per unit | Windows |
|---|---:|---:|---:|
| Healthy | 35 | 360 | 12,600 |
| Injected | 2 | 540 (fault-injection only) | 1,080 |
| **Total** | **37** | — | **13,680** |

Training windows = **12,600** (healthy units only).

The ideal scenario yields 2,100 healthy trials plus 180 injection trials = **2,280 trials**. Total windows are 12,600 healthy + 1,080 injection = **13,680**. The schedule requires 210 healthy unit-visits over approximately 26 weeks, or about 8 unit-visits per week with two kits.

**Table 3.2. Minimum sampling scenario (20 healthy + 2 injected units; V = 3; T = 10; W = 6).**

| Group | Units | Windows per unit | Windows |
|---|---:|---:|---:|
| Healthy | 20 | 180 | 3,600 |
| Injected | 2 | 432 (fault-injection only) | 864 |
| **Total** | **22** | — | **4,464** |

Training windows = **3,600** (healthy units only).

The minimum scenario yields 600 healthy trials plus 144 injection trials = **744 trials**. Total windows are 3,600 healthy + 864 injection = **4,464**. The schedule requires 60 healthy unit-visits over approximately 26 weeks (about 2–3 unit-visits per week). Approximately 3,600 healthy windows is sufficient for Isolation Forest, One-Class SVM, and GMM, but thin for the Autoencoder and CNN. If the CNN underperforms, the tabular vibration-feature fallback (RMS, kurtosis, peak frequency) will be used.

#### Fault-injection sampling

Each injected unit is measured in three phases per fault type: **pre-injection, post-injection, and recovery**, with T_phase trials per phase (T_phase = n: 8 minimum, 10 ideal), yielding n pre/post pairs. The three fault types are blocked return air, reduced refrigerant (requires a licensed technician and a one-time supervised procedure), and misaligned fan blade. Fault injection will be performed only with campus facilities permission and under supervised conditions.

The four sensor groups are ambient, current/power, vibration, and airflow. With 12 tests (4 sensor groups × 3 fault types) and Holm correction, the strictest cutoff is 0.05 / 12 = 0.0042. The smallest one-sided exact Wilcoxon p-value with n pre/post pairs is 1 / 2^n, so **n ≥ 8 pairs** is required (1/256 = 0.0039), i.e., at least 8 trials per phase.

**Table 3.3. Fault-injection sampling per injected unit.**

| Scenario | Trials per phase (n) | Trials per unit (n × 3 phases × 3 faults) | Windows per unit |
|---|---|---|---|
| Ideal | 10 | 90 | 540 (W = 6) |
| Minimum | 8 | 72 | 432 (W = 6) |

Rules:

- Spread trials across several sessions or days, not back-to-back.
- Pair pre-injection trial k with post-injection trial k under matched conditions.
- Analyze each injected unit separately; do not pool units.
- Exclude injected units from training; use them only at scoring time.

#### Summary of sampling scenarios

**Table 3.4. Minimum and ideal sampling parameters.**

| Parameter | Minimum | Ideal |
|---|---|---|
| Healthy units | 20 | 35 |
| Injected units | 2 | 2 |
| Total units | 22 | 37 |
| Visits per healthy unit (V) | 3 | 6 |
| Trials per visit (T) | 10 | 10 |
| Windows per trial (W) | 6 | 6 |
| Windows per healthy unit | 180 | 360 |
| Healthy windows | 3,600 | 12,600 |
| Injection windows | 864 | 1,080 |
| Total windows | 4,464 | 13,680 |
| Training windows | 3,600 | 12,600 |
| Pre/post pairs per fault type | 8 | 10 |

Training uses healthy windows only. Total windows include the separate fault-injection windows in Table 3.3.

#### Implementation notes

- Store metadata with every window: `unit_id`, `visit_id`, `trial_id`, `window_index`, `phase` (pre/post/recovery/normal), `fault_type`, `timestamp`, and `kit_id`.
- Compute window features from raw samples; aggregate window scores to one trial score by median.
- The training-window formula assumes all healthy units are normal-condition; if a healthy unit is judged degraded during baseline inspection, exclude it from training and reduce the training count accordingly.
- Fit standardization and PCA on normal-condition training units only; apply the fitted transforms to held-out and injected units without refitting.
- Split training and test data by **unit**, not by window or trial, to prevent leakage.
- State explicitly in the thesis that statistical power comes from trials, not windows. Adding windows increases training rows but not independent evidence.
- For H1a, use one trial score per trial, a one-sided Wilcoxon signed-rank test, n ≥ 8 matched pre/post pairs per fault type, and Holm correction across the 12 sensor-group × fault-type tests within each injected unit. Report each injected unit separately; do not pool units.
