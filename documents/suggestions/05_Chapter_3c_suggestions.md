# Chapter III (Part 3): Model Development — Suggestions & Loopholes

## Loopholes

### L1. Excessive Textbook-Style Content

This section reads more like a **machine learning textbook chapter** than a research methodology. It explains the fundamentals of:
- Linear regression → loss functions → gradient descent
- Shallow neural networks → ReLU → hidden layers
- DNN architecture → binary cross entropy → SGD → backpropagation
- CNN → 1D convolution → 2D convolution → pooling → AlexNet
- k-NN → Minkowski distance
- Decision Trees → entropy / Gini / information gain
- Random Forest → bagging
- XGBoost → boosting
- SVM → kernels → hyperplanes

For a thesis methodology, this level of detail is unnecessary. A methodology chapter should describe **what** models are used and **how** they are configured — not re-derive their mathematical foundations. The derivations belong in an appendix or should be drastically condensed.

**Roughly 40 pages of this ~65-page section is textbook content that could be cut to 5–10 pages.**

### L2. No Actual Model Architectures Proposed

Despite extensive theoretical exposition, the section never specifies:
- **DNN:** How many hidden layers? How many neurons per layer? What activation functions (only ReLU is mentioned)? Dropout rate? Learning rate? Batch size? Optimizer (SGD vs Adam)?
- **CNN:** What architecture? Input image resolution? Number of convolutional layers? Filter sizes? Number of filters per layer? FC layer dimensions? Is it a custom architecture or a transfer learning model (e.g., MobileNetV2 for ESP32-CAM)?
- **Hybrid RF+CNN:** How are the two models combined? Does CNN extract image features that feed into RF alongside sensor data? Or are predictions averaged? This "hybrid" model is listed as a key objective but its architecture is never defined.

### L3. No Computational Resource Discussion

Training CNN and DNN models requires computational resources. The methodology doesn't mention:
- What hardware will be used for training (local PC, Colab, university cluster)?
- GPU availability?
- Expected training time per model.
- Memory constraints.

This is especially relevant for the CNN (image classification) which can be GPU-intensive.

### L4. Hybrid RF+CNN Model Architecture Undefined

The specific objectives (1.3) list "Hybrid Model: Random Forest and CNN" as a model to test. The literature review (2.9, Abood et al.) describes a CNN-GAN hybrid. But the model development section never explains how the RF+CNN hybrid works:

- Is the CNN used for image feature extraction, with its penultimate layer output fed into RF as features?
- Is the CNN used for image classification only, with its prediction (frost/coil condition) combined with RF's sensor-based prediction via ensembling?
- Is there a shared representation that both models contribute to?

**This is a critical gap** — the hybrid model is the most novel contribution but has no architectural definition.

### L5. No Model Selection Justification

Six models are listed for comparison (RF, XGBoost, k-NN, RBF SVM, DNN, Hybrid RF+CNN). The methodology doesn't justify:
- Why these specific 6 and not others (Logistic Regression, Naive Bayes, Gradient Boosting without XGBoost)?
- Why RBF kernel specifically for SVM (not linear or polynomial)?
- Why not compare against an autoencoder-based anomaly detection approach (reviewed favorably in 2.5)?

### L6. The CNN Is Used for Image Classification But Never Integrated

The CNN is described for ESP32-CAM image classification (frost, coil condition). But the 6 comparison models are for the **sensor data classification** (normal/abnormal). The relationship between:
1. CNN (image → nominal features: frost, coil condition)
2. ML models (sensor data + nominal features → normal/abnormal)

is never clearly stated as a two-stage pipeline. Is the CNN a preprocessing step or a separate model being compared?

### L7. No Overfitting Mitigation for DNN/CNN

The section mentions overfitting for Decision Trees (pruning) and Random Forest (averaging), but not for the DNN and CNN. Relevant techniques are missing:
- **Dropout** layers.
- **Early stopping** based on validation loss.
- **L2 weight regularization**.
- **Data augmentation** for the CNN (image rotations, brightness adjustments).
- **Batch normalization**.

### L8. Hyperparameter Tuning Is Too Generic

The 8-step tuning process described is generic and doesn't specify:
- Which hyperparameters will be tuned for each model.
- The search strategy (Grid Search? Random Search? Bayesian optimization?).
- The hyperparameter ranges/spaces.
- Whether the same CV folds are used for tuning and final evaluation (should be nested CV to avoid bias).

## Suggestions for Improvement

### S1. Drastically Condense Theoretical Content
Move the mathematical derivations (linear regression, gradient descent, backpropagation, convolution operations) to an appendix. Keep in the main text only:
- 1–2 paragraphs per model describing what it is and why it's relevant.
- A table of the specific architecture/hyperparameters used.

### S2. Define the Hybrid RF+CNN Architecture
Explicitly describe:
- Input: sensor data (9 continuous features) + CNN image features (from penultimate layer or CNN predictions).
- CNN branch: ESP32-CAM image → CNN → feature vector.
- Sensor branch: 9 continuous features → RF.
- Fusion: concatenation of CNN features + sensor features → RF for final normal/abnormal classification.
- Include an architecture diagram.

### S3. Specify DNN and CNN Architectures
Provide a table like:

| Model | Architecture | Hyperparameters |
|-------|-------------|----------------|
| DNN | Input(11) → Dense(64, ReLU) → Dropout(0.3) → Dense(32, ReLU) → Dense(1, Sigmoid) | lr=0.001, Adam, batch=32, epochs=100, early stopping |
| CNN | Input(240×240×3) → Conv2D(32,3×3) → MaxPool → Conv2D(64,3×3) → MaxPool → Flatten → Dense(128) → Dense(2, Softmax) | lr=0.0001, Adam, batch=16, epochs=50, augmentation |

### S4. Clarify the Two-Stage Pipeline
Make it explicit that the system is a **two-stage pipeline**:
- Stage 1: ESP32-CAM images → CNN → nominal features (frost yes/no, coil condition).
- Stage 2: Sensor data (9 continuous) + Stage 1 output (2 nominal) → ML model → normal/abnormal.
- Draw this as a flow diagram.

### S5. Add Overfitting Mitigation Strategies
For each model, list the specific techniques:
- DNN: Dropout (0.2–0.5), L2 regularization, early stopping (patience=10).
- CNN: Data augmentation (flip, rotate, brightness), Dropout, transfer learning.
- RF/XGBoost: max_depth, min_samples_leaf, n_estimators (already somewhat covered).
- k-NN: appropriate k, distance weighting.
- SVM: C parameter, gamma tuning.

### S6. Specify Hyperparameter Search Strategy
State clearly:
- Method: Grid Search or Random Search with 5-fold CV.
- For each model, list the hyperparameters and their search ranges.
- Use **nested cross-validation** (outer CV for evaluation, inner CV for tuning) to avoid optimistic bias.

### S7. Address Computational Resources
Add a short paragraph:
- Training environment (e.g., "Models trained on a PC with NVIDIA GTX 1660 Ti, 16GB RAM" or "Google Colab with T4 GPU").
- Expected training time per model.
- Framework: which library (scikit-learn, PyTorch, TensorFlow/Keras)?