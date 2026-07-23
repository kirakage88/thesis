# Chapter III (Part 2): Data Preprocessing

> Based on Hossain (2023) and Raschka et al. (2022).

## 3.2 Data Preprocessing

### 3.2.1 Data Cleaning

Raw sensor readings are checked for:
- **Missing data** — incomplete or duplicated entries removed regardless of severity.
- **Outliers** — ignored or removed depending on severity.
- **Sudden spikes** — handled as noise.

This step is critical because the PdM model depends on accurate patterns in temperature, humidity, current, and voltage measurements.

### 3.2.2 Data Splitting

Two methods are used and compared:

#### Holdout Method

Dataset split into 3 parts:
- **Training:** 60% — used to train the model.
- **Validation:** 20% — unseen during training, used to tune hyperparameters.
- **Test:** 20% — unseen, used for final performance evaluation.

#### k-Fold Cross-Validation

Training set split into k folds (without replacement). For each fold:
- k−1 folds used for training.
- 1 fold (test fold) used for performance evaluation.
- Repeated k times → k models and performance estimates.
- **Average performance** across folds is less sensitive to sub-partitioning than holdout.

Used for model tuning — finding optimal hyperparameters that yield satisfying generalization performance.

#### Combined Strategy for This Research

1. First split using **holdout: 80/20** (80% for training+validation, 20% for final testing).
2. The 80% portion is used with **5-fold cross-validation**.
3. Final 20% holdout is the true unseen test set.

### 3.2.3 Data Transformation

The dataset contains mixed variable types:
- **Continuous** with different scaling: current, temperature, humidity.
- **Categorical (nominal):** frost build-up, coil condition.

#### Data Encoding

**One-hot encoding** (dummy encoding) for nominal categorical variables:
- Transforms each nominal variable into multiple binary columns (dummy variables).
- Example: frost build-up → `frost_yes`, `frost_no`.

#### Feature Scaling — Standardization

When features have different ranges, they cannot be compared directly. **Standardization** transforms all features to:
- Mean (μ) = 0
- Standard deviation (σ) = 1

Formula: `z = (x − μ) / σ`

This is applied to all continuous variables before model training.

### 3.2.4 Data Reduction

The dataset has **p = 11 features** — too many can cause slow computation and overfitting. **Dimensionality reduction** reduces features while retaining key information.

#### Feature Extraction vs. Feature Selection

This research uses **feature extraction** — creating new features by combining/transforming original features.

#### Principal Component Analysis (PCA)

A linear algebra technique that converts correlated variables into uncorrelated **principal components**, reducing dimensionality while preserving as much variance as possible.

**PCA Steps:**

1. **Standardize** the training dataset (already done in 3.2.3).
2. **Compute the covariance matrix** to see how features relate:
   - `cov(x, y) = (1/m) × Σ(x_i − x̄)(y_i − ȳ)`
3. **Calculate eigenvalues (λ) and eigenvectors (v)** of the covariance matrix:
   - `C × v = λ × v`
   - Eigenvectors = **principal components**. Eigenvalues = their magnitude (importance).
4. **Sort eigenvalues** by decreasing magnitude.
5. **Plot variance explained ratio:**
   - `Explained variance ratio of λⱼ = λⱼ / Σ(all λ)`
6. **Select top k eigenvectors** where **cumulative explained variance ≥ 95%**.
7. **Construct projection matrix W** by horizontally stacking top k eigenvectors.
8. **Transform the dataset:** `X' = X × W`

Additionally, PCA can measure **feature importance through loadings** — the values within each eigenvector/principal component, where each row corresponds to one variable.
