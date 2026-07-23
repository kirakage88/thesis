# Chapter I: Introduction

## 1.1 Background of the Study

Air conditioning is essential for thermal comfort in hot/humid climates like the Philippines, but accounts for a large share of building energy consumption. Split-type ACs are widely used for their efficiency and compact design. The evaporator coil is critical — its condition directly affects cooling performance, energy use, and system lifespan.

Evaporator coils degrade from dust, corrosion, microbial growth, refrigerant issues, and poor maintenance. A study by Niknami et al. (2024) shows that fouling just **30% of an evaporator surface** causes a **13.5% drop in EER**, a **6.4% increase in energy consumption**, and a **19.1% reduction in cooling load**.

Traditional maintenance at Xavier University is limited to periodic cleaning by third-party contractors every 3–4 months. There is no continuous condition monitoring, and faults (leaks, vibration issues) have been observed within 2 months of servicing. This creates a gap: no data-driven early warning system exists.

This study aligns with **RA 11285** (Energy Efficiency and Conservation Act), which mandates energy-efficient technologies in both public and private sectors.

Predictive Maintenance (PdM), powered by AI/ML and IoT, provides a proactive solution by analyzing real-time sensor data to anticipate failures before they occur.

### Research Questions

1. How effective are the chosen data preprocessing and statistical feature selection techniques in identifying relevant input data from IoT sensors and system logs?
2. Which predictive model demonstrates the highest reliability in classifying the system as normal or abnormal?
3. How can the proposed framework integrate real-time data collection and model analysis into a cloud-based or self-hosted proactive maintenance workflow?

## 1.2 Main Objective

Design and develop a predictive maintenance model for coiled evaporators in split-type AC systems using AI techniques. Analyze critical operational parameters (air temperature, ice build-up, compressor current, supply voltage) to classify system condition as **normal** or **abnormal** and optimize maintenance schedules.

## 1.3 Specific Objectives

1. Establish a data acquisition and preprocessing pipeline with statistical feature selection/extraction to ensure input data quality and relevance.
2. Select and validate the top-performing predictive model by comparing: **Hybrid RF+CNN, XGBoost, k-NN, RBF SVM, DNN** using precision, sensitivity, and F1 scores.
3. Propose a Maintenance 4.0 framework using cloud-based or self-hosted workflow integrating real-time data collection, model analysis, and system monitoring.

## 1.4 Conceptual Framework

- **Independent variables:** Air temperature, noise, ice build-up, refrigerant leaks — operational indicators of system health.
- **Mediating variable:** The ML model (AI techniques + IoT data acquisition) — transforms raw sensor data into actionable insights.
- **Dependent variable:** Predictive maintenance outcome — the model's ability to accurately forecast failures and support proactive maintenance.

The framework emphasizes that the AI model is the mechanism that translates raw sensor readings into maintenance decisions.

## 1.5 Limitations

1. **Time-constrained data collection:** Natural coil fouling takes weeks/months. The study uses cloth/mesh to simulate fouling in a short timeframe, which doesn't perfectly replicate real dust accumulation or corrosion.
2. **Budget sensor accuracy:** Low-cost sensors with ±2–5% error margins introduce noise into the dataset, increasing false alarm/missed fault risk.
3. **Setup cost and integration challenges:** Multiple sensor installation and coordination is technically and financially demanding. Limited infrastructure constrains integration complexity.
4. **Modeling complexity vs. student expertise:** Models are limited to binary classification (normal/abnormal). Regression-based approaches require more advanced skills and higher-precision sensors.

Despite these limitations, the study provides a viable foundation for PdM in coiled evaporators using readily available resources.

## 1.6 Definition of Terms

Key terms defined include: Anomaly Detection, Artificial Intelligence, Coiled Evaporator, CNN, Dataset, Feature Extraction, Heat Map, Ice Build-Up, IoT, Machine Learning, Model Accuracy, Neural Network, Noise (acoustic), Overfitting, Predictive Maintenance, Random Forest, Refrigerant Leak, Sensor Data, Split-Type AC System, Temperature, and Validation.
