# Chapter IV: Results and Discussion

> Note: This chapter reports the **completed sensor calibration experiments**. The 6-month data collection and ML model results are not yet included.

---

## 4.1 Sensor Validity Experiments

### 4.1.1 BME280 Calibration

**Methodology:** 100 samples collected in a controlled environment. Linear regression performed in R — comparing BME280 readings against a reference indoor thermometer.

#### Temperature Calibration

**R Input:**
```r
model = lm(temp_device ~ temp_sensor - 1)
summary(model)
```

**Results:** Statistically significant (p < 0.05).

**Calibration Equation:**
```
Reference = Sensor × 1.0294412
```

- R² = 1.0 (near-perfect fit)
- Residual standard error: 0.1329 on 99 DF
- F-statistic: 3.646×10⁶ (p < 2.2×10⁻¹⁶)

The BME280 readings are multiplied by 1.0294412 to align with the reference thermometer. This is a slope-only (no-intercept) model.

#### Humidity Calibration

**Results:** Statistically significant (p < 0.05).

**Calibration Equation:**
```
Reference = Sensor × 1.0579399
```

- R² = 0.9999
- Residual standard error: 0.3348 on 99 DF
- F-statistic: 1.496×10⁶ (p < 2.2×10⁻¹⁶)

### 4.1.2 DS18B20 Calibration

**Methodology:** 100 samples from each of two conditions — normal and cold environments. Combined dataset used for linear regression per probe (A, B, C).

#### Probe A Calibration

**R Input:**
```r
modelA = lm(Probe_A$Reference ~ Probe_A$Sensor)
summary(modelA)
```

**Calibration Equation:**
```
Reference = 1.701471 + 0.984997 × Sensor
```

- R² = 0.9839
- Residual standard error: 0.7182 on 198 DF
- F-statistic: 1.212×10⁴ (p < 2.2×10⁻¹⁶)
- Both intercept (1.701471) and slope (0.984997) are statistically significant.

#### Probe B Calibration

```
Reference = 1.637417 + 0.9783362 × Sensor
```

- R² = 0.9998
- Residual standard error: 0.07977 on 198 DF
- F-statistic: 1.236×10⁶ (p < 2.2×10⁻¹⁶)

#### Probe C Calibration

Uses the same formula as Probe B:
```
Reference = 1.637417 + 0.9783362 × Sensor
```

---

## Summary of Calibration Factors (Verified)

| Sensor | Formula | R² |
|--------|---------|-----|
| BME280 Temperature | `raw × 1.0294412` | ~1.0 |
| BME280 Humidity | `raw × 1.0579399` | ~1.0 |
| DS18B20 Probe A | `1.701471 + 0.984997 × raw` | 0.9839 |
| DS18B20 Probe B | `1.637417 + 0.9783362 × raw` | 0.9998 |
| DS18B20 Probe C | `1.637417 + 0.9783362 × raw` | (same as B) |

All models are statistically significant (p < 2.2×10⁻¹⁶). These factors are hardcoded in all sensor sketches across the firmware codebase.

---

## Gaps / Not Yet Available

- ACS712 current calibration results.
- ZMPT101B voltage calibration results.
- ESP32-CAM image classification model training results.
- 6-month sensor data collection.
- ML model comparison (RF, XGBoost, k-NN, RBF SVM, DNN, Hybrid RF+CNN).
- Friedman test statistical comparison.
- Streamlit dashboard implementation.
