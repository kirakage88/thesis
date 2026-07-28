## Executive Summary

If I were reviewing this as a bachelor's thesis in Mechanical Engineering, I would recommend **Option B (Unsupervised Anomaly Detection)**, but with an important caveat:

> **Do not claim that you are diagnosing faults. Claim that you are prioritizing inspections by identifying units whose operating behavior deviates from their learned normal behavior.**

That distinction is critical. It aligns with your revised research gap, your non-invasive constraint, and the available data.

---

# 1. Recommendation: Option B (Unsupervised Anomaly Detection)

I recommend **Option B**, primarily because it is more consistent with the realities of your dataset and the claims your system can legitimately make.

## Reason 1: Your labels are not truly ground truth

The biggest weakness of Option A is not class imbalance.

It is **label quality**.

Your proposed labels come from:

> technician performs a brief visual inspection.

But your sensors measure:

* temperature
* electrical behavior
* vibration

while the technician observes:

* external condition
* apparent operation
* perhaps cooling performance

Neither directly measures the actual evaporator condition.

This means your classifier would be learning from labels that are themselves uncertain.

Machine learning cannot outperform unreliable ground truth.

---

## Reason 2: Your dataset naturally favors anomaly detection

Look at the numbers.

* 2,599 campus AC units
* only 13 documented problematic units

That immediately suggests

> failures are rare.

Rare failures are precisely the scenario where anomaly detection is commonly applied.

Rather than trying to learn every possible failure,

the model learns

> "this is what healthy operation normally looks like."

Anything sufficiently different is flagged.

That fits your data much better.

---

## Reason 3: It matches the thesis framing

Your revised thesis no longer claims

> predictive maintenance replaces scheduled maintenance.

Instead it claims

> assist maintenance staff in deciding which units deserve inspection.

That is exactly what anomaly detection produces.

Not

> "compressor failure."

But

> "this unit behaves unusually compared with the rest."

That is a realistic engineering contribution.

---

## Reason 4: The non-invasive limitation

External sensors are indirect measurements.

They cannot observe

* coil fouling directly
* refrigerant state
* fin condition

Therefore,

trying to assign precise diagnostic labels ("Normal" vs. "Abnormal") may overstate what the data supports.

Anomaly detection makes a more modest—and therefore more defensible—claim:

> "The operating signature has deviated from the learned baseline."

That is much easier to justify.

---

## Reason 5: Better long-term scalability

Suppose Xavier expands this system to hundreds of buildings.

Would they realistically inspect every unit every week to generate labels?

No.

An anomaly detection system scales much more naturally because it requires minimal manual labeling.

---

# 2. Strongest Argument for Option A

Despite recommending Option B, Option A has one major advantage that should not be underestimated.

## It answers a much clearer engineering question.

Maintenance personnel think in categories.

They want to know:

* Is this unit okay?
* Should I inspect it?

Not

> anomaly score = 0.71

A supervised classifier directly produces the language that maintenance staff already use.

It is easier to explain.

It is easier to evaluate.

It is easier to compare with literature.

It is easier to publish.

If high-quality labels were available,

I would almost certainly recommend Option A.

The problem is that your labels are not high-quality.

---

# 3. Validation Strategy for Option B

This is the biggest challenge.

Without labels,

how do you demonstrate the model is useful?

The answer is:

**validate from multiple perspectives rather than relying on a single metric.**

---

## Layer 1 — Historical Validation

Use the maintenance records.

For every documented defective unit,

ask:

> Did the anomaly score increase before or near the documented maintenance event?

This demonstrates practical usefulness.

---

## Layer 2 — Technician Verification

Each week,

inspect the highest anomaly-scoring units.

For example,

inspect

Top 5 most anomalous units.

Record whether technicians observe:

* abnormal vibration
* poor cooling
* unusual current
* excessive noise
* visible issues

This estimates the precision of the anomaly ranking.

---

## Layer 3 — Time-Series Consistency

Healthy units should exhibit relatively stable anomaly scores.

Units approaching maintenance should show:

* increasing anomaly trend
* sudden spikes
* persistent deviations

The trajectory itself becomes evidence.

---

## Layer 4 — Maintenance Reset

One particularly compelling validation:

Suppose

Week 8

High anomaly

Week 9

Cleaning

Week 10

Low anomaly

That demonstrates the model responds to maintenance interventions.

This is arguably stronger evidence than a single classification accuracy value because it shows the model tracks operational changes.

---

## Layer 5 — Ranking Metrics

Instead of emphasizing Accuracy or F1,

evaluate ranking quality.

Examples include:

* Precision@K (How many of the top-ranked anomalies were confirmed during inspection?)
* Recall@K (How many known problem units appeared among the highest anomaly scores?)
* Mean Average Precision (if labels are sufficient)
* ROC-AUC using the limited historical fault labels as a retrospective evaluation

This aligns better with a triage objective, where prioritization matters more than assigning a definitive class.

---

# 4. Additional Recommendation: Use Semi-Supervised Learning

I actually think there is a stronger third option.

Not purely supervised.

Not purely unsupervised.

Instead:

> **Semi-supervised anomaly detection.**

Workflow:

1. Train on predominantly normal data.
2. Detect anomalies.
3. Technician verifies only the flagged units.
4. Verified examples become labeled data.
5. Periodically retrain.

This closely resembles how predictive maintenance systems are deployed in industry and makes efficient use of limited inspection resources.

For a bachelor's thesis, however, this may introduce unnecessary complexity unless you frame it as future work.

---

# 5. Which Option Is Easier to Defend?

This is different from asking which is technically better.

I believe **Option A is easier to defend** in an undergraduate thesis defense.

Why?

Because examiners are accustomed to supervised learning.

Typical questions become:

* What was your accuracy?
* What was your F1-score?
* Which classifier performed best?
* Why did Random Forest outperform SVM?

Those are familiar discussions with clear quantitative answers.

By contrast, Option B invites more conceptual questions:

* What defines an anomaly?
* How do you know an anomaly is a fault?
* Could weather cause anomalies?
* Why isn't this just detecting environmental variation?
* What threshold defines an anomaly?
* How did you select that threshold?

These are valid questions, but they require a more nuanced understanding of anomaly detection and its limitations.

---

# My Overall Concern

There is one issue that affects **both** options and deserves more attention than the choice of learning paradigm.

Your proposal repeatedly refers to:

> "Normal" and "Abnormal."

However, **what exactly constitutes an abnormal unit is not operationally defined**.

Before selecting any machine learning method, establish a clear labeling or validation protocol. For example:

* A unit is considered **Normal** if it exhibits acceptable cooling performance, no abnormal vibration or electrical behavior during inspection, and no maintenance concern is recorded.
* A unit is considered **Degraded** if technician inspection identifies performance degradation, abnormal electrical or vibration characteristics, or if a maintenance record documents a fault requiring corrective action.

Without such an operational definition, supervised models lack reliable ground truth, and unsupervised models lack a meaningful benchmark for evaluation.

---

## Final Recommendation

If the objective is to produce the **most scientifically defensible methodology**, **Option B (Unsupervised Anomaly Detection)** is the stronger choice because it aligns with the available data, the rarity of faults, the non-invasive sensing approach, and the thesis's revised goal of serving as a **maintenance triage tool** rather than a fault diagnosis system.

If the objective is to produce the **easiest thesis to defend before an undergraduate panel**, **Option A (Supervised Classification)** is simpler to communicate and evaluate—but only if you can substantially improve the quality and consistency of your labels. As currently described, the labeling strategy is the weakest component of the supervised approach.
