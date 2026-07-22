# Chapter II: Review of Related Literature

The chapter surveys 10 studies spanning AI-driven PdM for HVAC, supervised ML for fault detection, deep learning for image-based diagnosis, and ensemble methods.

---

## 2.1 Tejani (2024) — AI-Driven PdM in HVAC Systems

**Key contribution:** Framework shifting HVAC maintenance from reactive/preventive to predictive using AI/ML.

- Core concepts: Condition-Based Monitoring (CBM) and Prognostics and Health Management (PHM).
- ML models used: SVM, Random Forest, K-Means Clustering, Q-Learning.
- Workflow includes: Data Preprocessing → Model Training & Validation → Integration with HVAC Systems.
- Architecture integrates sensor networks, real-time data pipelines, and AI predictive engines.
- Unresolved issues: scalability, data integrity, ethical governance.

## 2.2 Trivedi et al. (2019) — Supervised ML for AC Fault Detection

**Key contribution:** Hardware prototype combining distributed sensing with supervised learning for fault classification.

- Faults detected: gas leakage, capacitor malfunction.
- Sensors: voltage and current transformers measuring real/reactive/apparent power and power factor.
- **Results:** Fine Decision Tree achieved **93.5% fault detection accuracy** and **93.6% load identification accuracy**, outperforming SVM.
- Architecture: sensor network → microcontroller → ML classifier → fault type identification.

## 2.3 Singh et al. (2023) — MPC + ML for HVAC PdM

**Key contribution:** Integrates Model Predictive Control (MPC), ML classification, and dynamic energy benchmarking.

- Dataset: Semiconductor Manufacturing Process (SECOM) dataset simulating HVAC behavior.
- Models: Random Forest and Logistic Regression for anomaly detection.
- **Results:** Random Forest achieved **94.5% accuracy**, outperforming SVM and Decision Trees.
- Demonstrated up to **83% cost savings** through optimized control.

## 2.4 Sulaiman et al. (2020) — ML for HVAC Fault Detection (FDD)

**Key contribution:** System-wide FDD approach comparing multiple ML classifiers.

- Three categories of FDD: model-based, signal-based, and data-driven (ML).
- ML algorithms surveyed: SVM (+ PCA), ANN, Deep Learning.
- Metrics: accuracy, precision, recall.
- Found MLP (Multi-Layer Perceptron) promising for system-level fault detection.
- Research gap: real-world large-scale validation and hybrid models.

## 2.5 Bouabdallaoui et al. (2021) — PdM in Building Facilities

**Key contribution:** PdM framework for building facility management using autoencoders.

- Data sources: Building Automation Systems (BAS), IoT sensors, CMMS, BIM.
- **Unsupervised deep learning** approach: autoencoders learn "normal" operating patterns and flag deviations.
- Anomaly score: RMSE between input vector and reconstructed output; threshold-based alerting.
- Framework: data collection → processing → model development → fault notification → model improvement.
- Key advantage: works with unlabeled data — critical given the scarcity of labeled fault data.

## 2.6 Sharma & Mistry (2023) — ML Algorithms for HVAC PdM

**Key contribution:** Comprehensive survey of ML techniques for HVAC predictive maintenance.

- Supervised: Decision Trees, Random Forests, SVM for normal/faulty classification.
- Deep Learning: CNN for thermal image faults, RNN for time-series degradation patterns.
- Workflow: data collection → preprocessing → feature selection → training → evaluation → integration.
- Real-world case study: shopping center (509,612 ft²) demonstrated energy savings.
- Trends: cloud platforms, IoT sensors, edge devices, real-time anomaly detection.

## 2.7 Song et al. (2023) — DPCA + VGG-PCA for Fault Diagnosis

**Key contribution:** Hybrid signal processing + deep learning approach.

- DPCA (Dynamic Principal Component Analysis) for feature enhancement from time-domain vibration signals.
- VGG-PCA model for fault classification.
- **Results:** DPCA improved correct rate by **16.38%** over raw time-domain data. VGG-PCA outperformed other CNNs by **>17% accuracy** with **~70% faster runtime**.
- Provided detailed parameter optimization strategy for practical implementation.

## 2.8 Aji et al. (2020) — Random Forest for Magnetic Sensor PdM

**Key contribution:** PdM applied to geophysical magnetic sensor networks.

- Uses total geomagnetic field component (F) to detect sensor degradation.
- **Results:** RF score up to **0.98**, MAE around **0.83** for forecasting maintenance needs.
- Application: BMKG (Indonesia) sensor network reliability.

## 2.9 Abood et al. (2023) — CNN-GAN for Electromechanical PdM

**Key contribution:** Hybrid CNN + Conditional GAN for industrial motor fault diagnosis.

- CNN for feature extraction, CGAN for data generation and classification.
- **Results:** F-score of **100** on asynchronous motor fault dataset, outperforming standalone CGAN and other DL models.
- Addresses multiclass fault diagnosis in electromechanical systems.

## 2.10 Sarker (2021) — ML Algorithms and Real-World Applications

**Key contribution:** Foundational overview of supervised learning algorithms.

- Covers: KNN, SVM, Decision Trees, Random Forest, XGBoost.
- Deep Learning: MLP, CNN (ConvNet), backpropagation.
- Classification analysis as a supervised learning paradigm.
- Provides theoretical foundation for model selection in this thesis.

---

## Synthesis for This Thesis

| Technique | Source(s) | Application in this thesis |
|-----------|-----------|---------------------------|
| Random Forest | [2], [3], [6], [8] | Main classifier for tabular sensor data |
| CNN | [7], [9], [10] | ESP32-CAM image classification (frost/coil condition) |
| SVM | [2], [4], [10] | Comparison baseline |
| XGBoost | [10] | Ensemble comparison model |
| DNN/MLP | [4], [10] | Deep learning comparison |
| k-NN | [10] | Lazy learner baseline |
| Autoencoders | [5] | Anomaly detection approach (reference) |
