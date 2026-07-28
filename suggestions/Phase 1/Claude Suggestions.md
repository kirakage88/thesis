# Claude Suggestions
### Review of Thesis Proposal: "Development of a Predictive Maintenance Model for Coiled Evaporators in Split-Type Air Conditioning Systems"

---

## 1. Critique — Logical Flaws & Unfalsifiable Claims

- **H1 (F1 ≥ 0.85)** is an arbitrary threshold with no baseline justification. Nothing explains why 0.85 rather than 0.75 or 0.90. On a small, imbalanced, single-site dataset, hitting an arbitrary number risks becoming a target you reverse-engineer (via oversampling or threshold tuning) rather than a genuine test. A defensible bar should be tied to what a maintenance team would consider "useful enough to act on," or to beating a majority-class baseline by a stated margin.

- **H2 (PCA-reduced ≈ full feature set)** is not a hypothesis that can fail in an interesting way. With only ~7 physical sensors and their derived features, PCA compressing "most of the variance" into fewer components is close to guaranteed — a statistics truism, not a domain finding. Feature *selection* (which measurements are diagnostic) is more scientifically interesting than dimensionality *reduction* here.

- **H3 (CNN-augmented beats tabular by ≥2% F1)** sets an oddly precise bar without justifying why 2% is the meaningful margin. With a likely small sample size, a 2% F1 difference is well within noise for many classifiers — this hypothesis may be undecidable given your data size rather than true or false.

- **H4 ("does not significantly degrade")** is a null-hypothesis-style claim, which is inherently harder to support with a small sample (absence of evidence ≠ evidence of absence). If the PMV experiment ends up underpowered — likely, since it depends on a DIY airflow sensor being finished in time — you cannot legitimately conclude equivalence, only "no significant difference detected." As written, this risks overclaiming a null result as validated equivalence.

- **The reframed research gap conflates two different gaps.** The first half (staff can't tell which units are degrading between visits) is a real operational gap. The second half ("prototype for scalable, localized predictive diagnostics" for "Campus of the Future") is aspirational and untested by anything in RQ1–RQ3. A single-site model trained on 30–40 units says nothing about scalability or transferability. This is scope-creep in the framing that isn't backed by the methodology, and a defense committee is likely to probe it.

---

## 2. Loopholes — Unaddressed Practical Problems

- **Class imbalance** is the single biggest unaddressed risk. If faults are rare enough that scheduled maintenance mostly catches them, the "Abnormal" class may end up with very few labeled instances. F1 ≥ 0.85 with, say, 5 abnormal units out of 35 is close to meaningless without specifying averaging method (macro/weighted/per-class) and a resampling or class-weighting strategy.

- **Ground truth labeling strategy is unspecified.** Is "Normal" vs. "Abnormal" based on a technician's subjective judgment during cleaning (label noise, possible circularity) or a measurable proxy (refrigerant pressure, temperature differential threshold)? This is arguably a bigger open question than any modeling choice.

- **The non-invasive constraint conflicts with the labeling problem.** Removing internal imaging (ESP32-CAM) is good for feasibility, but it also removes your best potential source of ground-truth evidence (visible leaks, corrosion, ice buildup). If labels ultimately come from invasive inspection at cleaning time, that should be stated explicitly in the methodology — using invasive data only to *generate* labels (not at inference time) is fine, but needs to be spelled out or a committee member may flag it as a contradiction.

- **Weekly-visit sampling regime has a serious temporal resolution problem.** The motivating observation is that faults can appear within 2 months of servicing. With 2 kits rotating across 30–40 units, each unit may be sampled only once every 2–4+ weeks depending on rotation logic (unspecified). The system may structurally be unable to catch fast-onset faults — the exact failure mode motivating the thesis.

- **Portable kits introduce measurement variability** the original permanently-installed design didn't have: mounting position/tightness for temp sensors, vibration sensor rigidity, ambient conditions at visit time. This is a confound the model may pick up on instead of true fault signatures, with no standardized mounting/measurement protocol mentioned.

- **CNN spectrogram approach (H3) likely needs more vibration data than a weekly, rotated setup will produce.** With only a handful of recordings per unit, expect severe overfitting risk, compounded by class imbalance.

- **PMV conditional branch is doing double duty** as both a "nice to have" and a hypothesis test (H4). It's gated on a DIY airflow sensor being finished in time, meaning H4/RQ3 could become entirely untestable. This should be framed unambiguously as a stretch goal, not core to the thesis's contribution.

- **No mention of train/test split strategy.** If all data comes from the same 30–40 units, splitting by observation rather than by unit risks the model learning to recognize *specific units* rather than generalizable *fault signatures* — inflating apparent performance.

---

## 3. Strengths of the Reframing

- Reframing as a **"complementary triage tool"** rather than a replacement for preventive maintenance is a smart move — both rhetorically (avoids an unwinnable argument with a skeptical adviser) and substantively (more honest about what a small-sample bachelor's thesis can demonstrate).
- **Dropping internal imaging and the 50-node permanent network** is a major feasibility win — far more realistic to actually execute and defend than the original design.
- **Being upfront that this is a single-site, locally-trained model** is honest and appropriately scoped, as long as the "Campus of the Future" scalability language is walked back or marked explicitly as future work.
- **The RQ1 → RQ2 → RQ3 structure** (feature selection → model comparison → optional metric substitution) is a sensible, incremental narrative rather than a grab-bag of unrelated experiments.

---

## 4. Suggested Rewrites

**RQ2 (sharper):**
> Among tree-based ensembles (RF, XGBoost), distance-based methods (k-NN, RBF SVM), and neural approaches (DNN, CNN-augmented), which classifier best distinguishes Normal from Abnormal AC units using only external, non-invasive sensor features — and does performance ranking hold consistently across unit types/capacities?

**H1 (tie threshold to something defensible):**
> At least one ML model achieves F1 significantly above a majority-class baseline classifier, with the specific improvement margin reported and interpreted relative to the observed class distribution.

**H3 (soften the arbitrary 2% threshold):**
> The CNN-augmented model shows a measurable, consistent F1 improvement over tabular-only models across cross-validation folds, even if the absolute margin is small given sample size constraints.

**H4 (reframe as exploratory, not confirmatory):**
> Exploratory: Does substituting a PMV-derived composite feature for raw environmental sensor readings change classification performance, and in which direction? (No directional hypothesis is asserted given dependency on an unvalidated DIY airflow sensor.)

**New RQ worth adding:**
> RQ4: Does classifier performance generalize across AC units held out entirely from training (unit-level split), or does performance degrade substantially compared to observation-level (random) splits — indicating unit-specific rather than fault-general learning?
