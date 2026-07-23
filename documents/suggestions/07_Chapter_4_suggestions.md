# Chapter IV: Results and Discussion — Suggestions & Loopholes

## Loopholes

### L1. Chapter Is Incomplete

Only sensor calibration results are reported. Missing:
- ACS712 current sensor calibration.
- ZMPT101B voltage sensor calibration (the 3rd-order polynomial).
- ESP32-CAM CNN training results (accuracy, confusion matrix).
- 6-month sensor data collection results.
- ML model comparison (RF, XGBoost, k-NN, RBF SVM, DNN, Hybrid RF+CNN).
- Friedman test results and statistical comparison.
- Streamlit dashboard implementation and screenshots.

This is acknowledged but the chapter structure should be planned now to ensure completeness.

### L2. Suspiciously Perfect R² = 1.0 for BME280 Temperature

The linear regression for BME280 temperature calibration reports:
- Multiple R² = 1.0
- Adjusted R² = 1.0
- F-statistic = 3.646×10⁶

An R² of exactly 1.0 is suspicious. Possible explanations:
- The no-intercept model (`~ temp_sensor - 1`) can produce inflated R² values because R² is computed differently without an intercept.
- The sensor readings (24.5–24.9°C) and reference readings (25.2–25.6°C) are very tightly clustered in a narrow range — a narrow input range with consistent sensor error can produce artificially high R².
- Data may have been inadvertently duplicated or the regression computed incorrectly.

**Action:** Verify the R² computation. Report the standard (with-intercept) R² alongside the no-intercept R². Include a residual plot to visually confirm the fit.

### L3. Probe A Has a Major Outlier

Probe A calibration results show:
- R² = 0.9839 (significantly lower than Probe B's 0.9998).
- Max residual = **−9.9523** (nearly 10°C deviation!).

Inspecting the data table (Appendix A.4), there are suspicious data points:
- Row showing `25.94 | 17.3` — the reference jumps from ~27°C to 17.3°C while the sensor reads 25.94°C. This looks like a **data entry error** (should be 27.3, not 17.3).
- Rows showing `14 | 15.4` — a sudden jump from ~25.6°C to 14°C in the sensor reading while the reference is 15.4°C. This is likely the "cold environment" trial boundary, but the transition appears abrupt without a label separating the two conditions.

**Action:**
- Investigate and correct the `17.3` data point (likely `27.3`).
- Clearly label the boundary between "normal" and "cold" environment trials in the data table.
- Report calibration results for the two conditions separately, then combined.

### L4. No Confidence Intervals on Calibration Coefficients

The regression outputs show the coefficient estimates but the methodology section doesn't mention:
- **95% confidence intervals** for slope and intercept.
- **Prediction intervals** for future sensor readings using the calibration.
- **Residual analysis** (normality of residuals, homoscedasticity).

These are standard in calibration studies and strengthen the validity claim.

### L5. No Independent Validation of Calibration

The calibration models are fitted on 100 samples (BME280) or 200 samples (DS18B20). But:
- No **held-out test set** is used to validate the calibration on unseen data.
- The R² reported is from the training data (in-sample), which is optimistically biased.
- No **cross-validation** is performed on the calibration regression.

**Action:** Split the calibration data into train/test (e.g., 80/20). Report R² and RMSE on the test set. This proves the calibration generalizes.

### L6. Probe B Shows a Different Formula Than Stated

The R output for Probe B shows:
```
(Intercept)  1.8443655
Probe_B$Sensor  0.9684665
```

But the thesis states (and the codebase uses):
```
Reference = 1.637417 + 0.9783362 × Sensor
```

The regression coefficients **don't match** the stated formula. This suggests either:
- The R output shown is from a different run/dataset than the final formula.
- The formula was updated after initial analysis but the R output wasn't refreshed.

**Action:** Reconcile the regression output with the final calibration formula. If the formula changed, update the R output shown in the document.

### L7. No Uncertainty Propagation Analysis

The calibrated sensor values feed into the ML models. But the calibration itself introduces **uncertainty** (the regression has residual error). The methodology doesn't discuss:
- How calibration uncertainty propagates through the ML pipeline.
- Whether the ML models are robust to the residual sensor noise.

This is a critical validity question — if the calibration residual std is 0.72°C (Probe A) and the ML model distinguishes normal from abnormal based on temperature differentials of ~2–3°C, the signal-to-noise ratio is concerning.

## Suggestions for Improvement

### S1. Plan the Complete Chapter Structure
Outline the full chapter now:
1. 4.1 Sensor Calibration (current) — BME280, DS18B20, ACS712, ZMPT101B.
2. 4.2 CNN Image Classification Results — accuracy, precision, recall, confusion matrix.
3. 4.3 Dataset Overview — class distribution, feature statistics, PCA results.
4. 4.4 ML Model Comparison — performance table (all 6 models, all 4 metrics).
5. 4.5 Statistical Analysis — Friedman test + Nemenyi post-hoc, CD diagram.
6. 4.6 Deployment Results — dashboard screenshots, inference latency, system reliability.

### S2. Fix BME280 R² Reporting
- Report both with-intercept and no-intercept R².
- Include a scatter plot of sensor vs. reference with the regression line.
- Include a residual plot to verify homoscedasticity.
- If R² = 1.0 persists, explain why (narrow input range, consistent sensor bias).

### S3. Investigate and Correct Data Errors
- Fix the `17.3` → `27.3` entry in Probe A data.
- Clearly separate and label "normal" vs. "cold" environment data.
- Report calibration per condition and combined.
- Consider removing or flagging outliers before regression.

### S4. Add Held-Out Validation for Calibration
Split each sensor's calibration data:
- 80% for fitting the regression.
- 20% for validation.
- Report R², RMSE, and max error on the validation set.

### S5. Reconcile Probe B Formula
Ensure the regression output shown in the document matches the formula used in the firmware codebase. If the formula was derived from a different dataset or run, document which one is canonical.

### S6. Add Calibration Uncertainty Discussion
For each sensor, report:
- Residual standard error (already in R output — interpret it).
- Expected accuracy after calibration (±X°C, ±Y%).
- Whether this accuracy is sufficient for the ML model's discrimination task.

### S7. Add Visualizations
For each calibration:
- Scatter plot: sensor reading (x) vs. reference (y) with regression line and 95% CI band.
- Residual plot: fitted values (x) vs. residuals (y) with a horizontal line at 0.
- Q-Q plot for residual normality.
- Bland-Altman plot (difference vs. mean) — standard in instrument comparison studies.