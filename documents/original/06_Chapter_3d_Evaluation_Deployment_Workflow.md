# Chapter III (Part 4): Model Evaluation, Deployment & Workflow

## 3.4 Model Evaluation

### Confusion Matrix

All classification models are evaluated via confusion matrix:

| | Predicted Positive | Predicted Negative |
|---|---|---|
| **Actual Positive** | True Positive (TP) | False Negative (FN) — Type II error |
| **Actual Negative** | False Positive (FP) — Type I error | True Negative (TN) |

### Performance Metrics

#### Accuracy
```
Accuracy = (TP + TN) / (TP + TN + FP + FN)
```
Proportion of correct predictions. Valid for **balanced** datasets only — can be misleading when classes are imbalanced.

#### Precision
```
Precision = TP / (TP + FP)
```
Ratio of correctly predicted positives among all positive predictions. Used when **low false positive rate** is critical.

#### Recall (Sensitivity)
```
Recall = TP / (TP + FN)
```
Ratio of correctly predicted positives among all actual positives. Used when **low false negative rate** is critical.

**Trade-off:** High precision → poor recall, and vice versa.

#### F1 Score
```
F1 = 2 × (Precision × Recall) / (Precision + Recall)
```
Harmonic mean of precision and recall. Used when both need to be considered simultaneously.

### Statistical Analysis

After k-fold cross-validation during training, the test split is grouped into **30 subsets**, each cross-validated across n models. Each model is evaluated on accuracy, precision, recall, and F1.

Since dataset accuracy typically ranges 80–95% (non-normal distribution), the **Friedman Test** is used — a non-parametric alternative to Repeated Measures ANOVA.

**Hypotheses:**
- H₀: The means across all models are equal.
- H₁: At least one population mean differs from the rest.

---

## 3.5 Model Deployment

The final phase transitions the trained model from a static saved file (`.pkl` or `.pth`) into a functional decision-support system displaying real-time health status of monitored AC units.

**Context:** University research prototype — prioritizes pragmatic, achievable deployment without complex enterprise infrastructure.

### 8.1 Deployment Architecture & Technology

Hosted on the central **Ingest Server** (already receiving data from all 50 Master ESP32 nodes).

#### Streamlit (Application Framework)
- Open-source Python framework for interactive data-driven web apps.
- **No HTML/CSS/JavaScript required** — suited for a mechanical engineering student.
- Dashboard displays model predictions and sensor data.

#### SQLite (Prediction Database)
- Serverless, self-contained database built into Python (`sqlite3` module).
- Stores entire database in a single file.
- Ideal for a research prototype — no database server installation overhead.
- Stores prediction history for all units.

#### Watchdog (Automation)
- Python library that monitors directories for file system events.
- Detects new file creation in raw data folder.
- Triggers automated prediction pipeline.

### 8.2 Deployment Workflow

Two connected components:

#### Component 1: Automated Inference Service

A persistent Python script running on the Ingest Server:

1. **Monitor:** Watchdog watches `02_Data/raw/` directory.
2. **Trigger:** When a Master ESP32 saves a new file (e.g., `20251116T110400Z_SBM-AVR_ACU-01_T03_RAW.csv`), the "file created" event fires.
3. **Execute Prediction Pipeline:**
   - a. Load and preprocess the new CSV: apply CCFs from calibration database, run preprocessing scripts.
   - b. Load the best trained model (e.g., `random_forest_final.pkl`) via `joblib`/`pickle`.
   - c. Call `model.predict()` on processed data → "Normal" or "Abnormal".
4. **Store:** Insert prediction into `predictions.db` SQLite table with Unit ID, timestamp, and result.

#### Component 2: Streamlit Dashboard (`app.py`)

Run via `streamlit run app.py` on the server:

1. **Database Connection:** On load, connects to `predictions.db` to retrieve latest data.
2. **Main Status Dashboard:** High-level overview of all 50 units. Most recent prediction per unit displayed in a color-coded table (Green = Normal, Red = Abnormal).
3. **Detailed Unit View:** Dropdown (`st.selectbox`) selects a specific unit (e.g., `COE_ACU-02`).
4. **Historical Analysis:** Fetches prediction history for the selected unit. Displayed via `st.line_chart` or `st.dataframe` — allows maintenance staff to review sensor trends (coil temp, compressor current) leading up to abnormal predictions.

---

## 3.6 General Project Workflow

The project follows a phased workflow integrating product/model deployment and software development, represented in flowchart and Gantt chart form.

**Key phases:**

1. **Sensor calibration** — validity experiments for BME280, DS18B20, ACS712, ZMPT101B.
2. **Hardware deployment** — install nodes on 50 AC units across 3 locations.
3. **6-month data collection** — weekly visits, 10 trials per unit.
4. **Data preprocessing** — cleaning, splitting, transformation, PCA.
5. **Model development** — CNN for images + 5 classifiers for sensor data.
6. **Model evaluation** — confusion matrices, Friedman test comparison.
7. **Model deployment** — Streamlit dashboard + SQLite + Watchdog automation.
