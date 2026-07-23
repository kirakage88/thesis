# Chapter III (Part 2): Data Preprocessing — Suggestions & Loopholes

## Loopholes

### L1. No Handling of Class Imbalance

The dataset will almost certainly be **imbalanced** — in real-world HVAC operation, units spend the vast majority of time in "Normal" condition. "Abnormal" events (frost, fouling, faults) are relatively rare, especially with only 6 months of data.

The preprocessing section mentions data cleaning, splitting, encoding, scaling, and PCA — but **never mentions class imbalance handling**. Training a classifier on imbalanced data without correction will bias the model toward the majority class (Normal), producing high accuracy but poor recall on the minority class (Abnormal) — which is the class that matters most for predictive maintenance.

### L2. No Temporal Feature Engineering

Sensor data is inherently **time-series** data. The preprocessing section treats each reading as an independent vector, with no mention of:
- **Rolling window statistics** (mean, std, min, max over a time window).
- **Rate of change** (δ temperature per minute — critical for frost detection).
- **Trend features** (is temperature increasing/decreasing over the trial?).
- **Lagged features** (temperature 5 minutes ago vs. now).

For detecting gradual degradation (fouling) or sudden onset (frost), temporal features are likely more predictive than instantaneous readings.

### L3. No Missing Data Imputation Strategy

Section 3.2.1 says incomplete or duplicated entries are "removed regardless of severity." This is problematic because:
- **Removing data reduces sample size** — already a concern given the limited monitoring period.
- **Sensor dropouts** (especially ACS712 noise, ESP32-CAM connectivity) will create gaps.
- **Removing entire rows** when one sensor has a missing reading wastes the valid readings from other sensors in that same timestamp.

**Better approach:** Impute missing values using:
- Forward-fill / linear interpolation for short gaps.
- Median/KNN imputation for longer gaps.
- Flag missing values with a binary indicator feature.

### L4. PCA Threshold (95%) Is Unjustified

The 95% cumulative explained variance threshold is stated but not justified. Why 95% and not 90% or 99%? The choice significantly affects:
- Number of principal components retained.
- Information loss vs. dimensionality reduction trade-off.

This should be a hyperparameter that's tuned, not a fixed value.

### L5. Data Leakage Risk in Standardization

Standardization requires computing mean (μ) and standard deviation (σ). The section doesn't specify:
- Are μ and σ computed on the **training set only** then applied to validation/test sets?
- Or on the **entire dataset** before splitting?

Computing statistics on the entire dataset before splitting causes **data leakage** — information from the test set bleeds into the training data via the scaling parameters. This inflates evaluation metrics.

### L6. No Discussion of Categorical Variable Handling Post-Image-Classification

The ESP32-CAM/CNN pipeline produces 2 nominal features (frost, coil condition). But these labels are themselves **predictions** from another ML model (CNN). The preprocessing section treats them as observed ground truth. Issues:
- CNN prediction errors propagate into the downstream classifier.
- The CNN's confidence score is lost — only the binary label is kept.

**Suggestion:** Consider using the CNN's probability output (e.g., 0.87 frost probability) as a continuous feature rather than the binary label.

### L7. No Cross-Validation Data Leakage Consideration

The combined strategy (80/20 holdout + 5-fold CV) is sound, but doesn't address:
- **Spatial autocorrelation:** Multiple AC units in the same building may experience similar ambient conditions. If units from COE Building are in both training and test sets, this creates leakage.
- **Temporal autocorrelation:** Consecutive readings from the same unit are correlated. Random splitting may put adjacent readings in different sets.

**Suggestion:** Use **grouped splitting** by AC unit (all readings from ACU-01 in either train or test, never both) and optionally **temporal blocking** (train on months 1–4, test on months 5–6).

## Suggestions for Improvement

### S1. Add Class Imbalance Handling Section
Add a subsection covering:
- Detection of imbalance (count per class).
- Strategy: SMOTE (Synthetic Minority Oversampling), class-weighted loss functions, or stratified sampling.
- Evaluation: report precision/recall/F1 per class, not just overall accuracy (already mentioned but should be linked here).

### S2. Add Temporal Feature Engineering Section
Create a subsection (e.g., "3.2.5 Feature Construction") covering:
- Window-based statistical features (mean, std, slope over each 10-trial session).
- Rate-of-change features (ΔT/Δt for inlet/outlet temp difference).
- Derived features (COP proxy = temp differential / compressor current).

### S3. Fix Standardization Order
Explicitly state: "Standardization parameters (μ, σ) are computed on the training split only and then applied identically to validation and test splits to prevent data leakage."

### S4. Justify or Tune the PCA Threshold
Either:
- Justify 95% with a reference, or
- Treat the threshold as a hyperparameter and report performance across thresholds (85%, 90%, 95%, 99%).

### S5. Add a Data Leakage Prevention Strategy
Describe the splitting strategy that prevents:
- Same-unit data appearing in both train and test (grouped splitting).
- Temporal correlation causing optimistic metrics (blocked temporal split).

### S6. Use CNN Confidence as Continuous Feature
Instead of passing binary frost/coil labels from the CNN to the downstream model, pass the CNN's probability output as a continuous feature. This:
- Preserves uncertainty information.
- Softens the impact of CNN misclassification.
- May improve downstream model performance.