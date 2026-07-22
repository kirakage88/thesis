# Chapter III (Part 3): Model Development

## 3.3 Model Development

The first stage involves classifying images (ESP32-CAM) into nominal features (frost, coil condition) using **CNN**, a type of deep learning for computer vision. The remainder of the sensor data feeds into the classification models.

The chapter builds from foundations upward: Neural Networks → Deep Neural Networks → CNN → traditional ML models.

---

### Neural Network Foundations

#### Deep Learning Basics

Deep Learning is a large subset of ML built upon supervised learning. The most basic form is the **perceptron** — a special type of linear regression using gradient descent.

**1D Linear Regression:**
```
y = b + wx
```
Parameters φ = [b, w] where b is the y-intercept, w is the slope.

**Loss Function:** Quantifies the mismatch between model predictions and ground truth. Sum of squared deviations:
```
L(φ) = Σ(f(x_i, φ) − y_i)²
```

**Goal:** Find parameters φ that minimize L(φ). This is done via **gradient descent** — iteratively moving downhill on the loss surface.

#### Shallow Neural Networks

Functions y = f(x, φ) mapping multivariate inputs to multivariate outputs. Broken into three parts:

1. Compute linear functions of input x: `θ₁₁x + θ₁₀`, `θ₂₁x + θ₂₀`, `θ₃₁x + θ₃₀`
2. Pass through **activation function** a(z). Most basic: **ReLU** — `a(z) = max(0, z)`
3. Combine hidden unit outputs linearly: `y = φ₀ + φ₁h₁ + φ₂h₂ + φ₃h₃`

Where hidden units: `hₖ = a(θₖ₁x + θₖ₀)`

**Layers terminology:**
- **Input layer** — receives x
- **Hidden layer** — contains hidden units (neurons)
- **Output layer** — produces y

With matrix notation, a network with n inputs (m × n) and p outputs uses:
```
h = a(X × W + b)
```

---

### Deep Neural Network (DNN)

DNNs have **more than one hidden layer**, giving them more descriptive power for high-dimensional data. More hidden layers = more linear regions to approximate any function.

General deep network with K layers:
```
h₀ = x
hₖ = a(Wₖ × hₖ₋₁ + bₖ)    for k = 1,...,K
y = Wₖ₊₁ × hₖ + bₖ₊₁
```

Parameters φ = {bₖ, Wₖ} for all K layers.

#### Binary Classification DNN (for this research)

- Multivariate inputs (sensor features).
- One output neuron with range [0,1].
- **Binary Cross-Entropy Loss** (BCE) — uses Bernoulli distribution and negative log-likelihood:
  ```
  BCE = −[y × log(sigmoid(z)) + (1−y) × log(1−sigmoid(z))]
  sigmoid(z) = 1 / (1 + e^(−z))
  ```

#### Training: Gradient Descent

1. Compute partial derivatives of loss: `∂L/∂φ`
2. Update parameters: `φ ← φ − α × (∂L/∂φ)`
   - α = learning rate (hyperparameter)
   - φ = parameters (learned automatically)

#### Stochastic Gradient Descent (SGD)

Instead of computing gradients on the entire dataset (expensive), SGD computes on a small, randomized batch. This reduces computational cost significantly.

#### Backpropagation

Combines **forward pass** (computing loss through layers) and **backward pass** (updating weights starting from the outermost layer inward).

- **Forward pass:** Sequential computation of h₁, h₂, ..., hₖ, y, loss.
- **Backward pass:** Compute derivatives of loss with respect to each layer's weights/bias in reverse order using the chain rule.

The model processes the dataset multiple times. Each complete pass = one **epoch**. The number of epochs is a key hyperparameter.

---

### Convolutional Neural Network (CNN)

CNNs have special **convolutional layers** that process each image region independently using parameters shared across the entire image — far fewer parameters than fully connected layers.

#### 1D Convolution

Transforms input x into output z where each zᵢ is a weighted sum of nearby inputs using a **kernel** (filter):
```
zᵢ = ω₁xᵢ₋₁ + ω₂xᵢ + ω₃xᵢ₊₁
```
Kernel: ω = [ω₁, ω₂, ω₃]

**Key characteristics:**
- **Padding:** Pad input with 0 or mirrored values.
- **Stride:** Skip every other input or by n inputs.
- **Kernel size:** Region size, typically odd to center around current position.

Output with bias b and activation a[z]: `z = a(ω ∗ x + b)`

#### Multi-Channel Convolutions

Instead of a single convolution, compute several in parallel. Each produces a new set of hidden variables called a **feature map** or **channel**.

If input has Cᵢ channels and kernel size K, each output channel is a weighted sum over all Cᵢ channels and K kernel entries. For Cₒ output channels: weights ω ∈ ℝ^(Cᵢ×Cₒ×K), biases b ∈ ℝ^Cₒ.

#### 2D Convolution (for images)

A 3×3 kernel ω ∈ ℝ³ˣ³ applied to 2D input:

```
hᵢⱼ = ΣᵤΣᵥ ωᵤᵥ × xᵢ₊ᵤ,ⱼ₊ᵥ
```

For RGB images (3 channels), a 3×3×3 kernel has 27 weights per output channel.

#### Pooling (Downsampling)

Scales down each feature map, removing unwanted features and reducing computation:
- **Max Pooling:** Retain maximum of each 2×2 input region.
- **Mean Pooling:** Take average.

#### Feature Hierarchy

- **Low-level features:** contours, edges, angles, colors (early layers).
- **High-level features:** items, faces, shapes, interactions (later layers) — built from low-level pairings.

#### AlexNet (Reference Architecture)

First convolutional network to perform well on ImageNet (2012):
- 8 hidden layers with ReLU activation.
- First 5 layers: convolutional → fully connected.
- Input: 1.28M training images, 1000 categories.

---

### k-Nearest Neighbors (k-NN)

A **lazy learner** — doesn't learn a discriminative function; instead memorizes the training dataset.

**Algorithm:**
1. Choose k and a distance metric.
2. Find k-nearest neighbors of the data point to classify.
3. Assign class label by **majority vote**.

**Distance metric:** Minkowski distance generalizes Euclidean and Manhattan:
- p = 2 → Euclidean distance
- p = 1 → Manhattan distance

**Critical:** Choosing the right k balances overfitting vs. underfitting. k-NN is susceptible to the **curse of dimensionality** — fails to generalize with too many features.

---

### Decision Tree (DT)

Attractive for **interpretability** — breaks down data by asking a series of yes/no questions.

#### Algorithm:
1. Start at tree root.
2. Split data on the feature that results in largest **Information Gain (IG)**.
3. Repeat at each child node until leaves are pure (all same class).
4. **Prune** the tree (set max depth) to prevent overfitting.

#### Information Gain:
```
IG(Xₚ, f) = I(Xₚ) − Σⱼ (Nⱼ/Nₚ) × I(Xⱼ)
```
Where I is the impurity measure.

**Binary trees** (used in scikit-learn): each parent splits into two children (X_left, X_right).

#### Impurity Measures:

| Measure | Formula | Usage |
|---------|---------|-------|
| **Entropy** | `I_H = −Σ p(i\|t) × log₂ p(i\|t)` | Splitting criterion |
| **Gini Impurity** | `I_G = 1 − Σ p(i\|t)²` | Minimize misclassification probability |
| **Classification Error** | `I_E = 1 − max(p(i\|t))` | Pruning criterion |

#### Overfitting Prevention:
- **Maximum depth:** Limits tree depth.
- **Minimum samples per leaf:** Ensures minimum data per leaf node.
- **Minimum samples per split:** Minimum samples to perform a split.
- **Minimum leaf nodes:** Controls leaf count.
- **Impurity threshold:** Stop when impurity falls below threshold.

---

### Ensemble Methods

Combine multiple small models — individually weak but collectively strong. Two types used:

1. **Bagging:** Models trained independently on different random data subsets. Combined by averaging (regression) or voting (classification).
2. **Boosting:** Models trained sequentially. Each new model fixes errors of previous ones. Final prediction = weighted combination.

#### Random Forest (RF) — Bagging

**Algorithm:**
1. Draw a random **bootstrap sample** of size n (randomly choose n examples with replacement).
2. Grow a decision tree from the bootstrap sample. At each node:
   - Randomly select d features without replacement.
   - Split using the feature that maximizes information gain.
3. Repeat k times (k = number of trees).
4. Aggregate predictions by **majority vote**.

**Advantage:** Robust to noise from averaging across trees. Don't need to prune. Only hyperparameter to tune: **number of trees k**. Larger k → better performance at computational cost.

#### XGBoost (eXtreme Gradient Boosting) — Boosting

Optimized implementation of gradient boosting. Builds trees sequentially, each correcting the previous tree's errors:

1. Train first decision tree.
2. Calculate error using loss function.
3. Train next tree on residuals.
4. Repeat.
5. Combine predictions.

Uses second-order gradients and advanced L1/L2 regularization to reduce overfitting.

---

### Support Vector Machine (SVM)

Finds the optimal **hyperplane** separating different classes by maximizing the margin.

**Key terms:**
- **Support vectors:** Data points closest to the decision boundary.
- **Margin:** Distance from hyperplane to nearest support vectors on each side.
- **Hard margin:** Maximizes distance while ensuring all points are correctly classified.

For binary classification with labels +1/−1:
```
Hyperplane: wᵀx + b = 0
Distance from xᵢ to boundary: |wᵀxᵢ + b| / ||w||
Classification: sign(wᵀxᵢ + b)
```

**Optimization goal:** `min ||w||² / 2` subject to `yᵢ(wᵀxᵢ + b) ≥ 1` for all i.

For non-linearly separable data, SVM uses **kernel functions** (linear, polynomial, RBF, sigmoid) to map data to higher-dimensional space. Drawback: performs poorly with noisy data and overlapping classes.

---

### Hyperparameter Tuning

Steps:
1. Visualize data and understand the problem.
2. Select best possible ML algorithm.
3. Split dataset into train/validation/test.
4. Determine hyperparameter space (HS).
5. Select search method (grid search, random search, etc.).
6. Implement cross-validation.
7. Evaluate model score.
8. Repeat 5–7 until best score achieved. Optimal hyperparameter set = best model score.

**Hyperparameters vs. Parameters:** Hyperparameters are set before training (tuned manually). Parameters φ are learned automatically during training.
