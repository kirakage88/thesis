# Critical Review: Coiled Evaporator Predictive Maintenance Thesis

## 1. CRITIQUE — Logical Flaws, Unfalsifiable Claims, Contradictions

### "Predictive" vs "Diagnostic" terminology mismatch (biggest conceptual issue)

The title says "Predictive Maintenance Model." But the methodology is cross-sectional classification: each weekly visit produces a single snapshot (Normal/Abnormal) at that moment. There are no time-series, no degradation trajectories, no failure-horizon forecasts ("unit X will fail within Y weeks"). Predictive maintenance implies *forecasting future state*; this study does *current-state diagnosis.* The reframed gap text ("triage tool," "flagging which units need attention") is actually more honest than the title. A panel member who knows the PdM literature will flag this immediately. Either rename it ("Condition-Based Monitoring" / "Non-Invasive Fault Classification") or restructure to actually do prediction — which, with this sampling regime, you can't.

### Circular gap logic

The gap states: "maintenance staff cannot identify which specific units are experiencing performance degradation between visits." This presupposes that (a) degradation is occurring between visits and (b) it produces externally detectable signals — both of which are precisely what the study needs to establish. The gap is real (you genuinely don't know what's happening between visits), but the framing presents degradation detectability as a given rather than an open question. A tighter gap would say: "The interval between services leaves maintenance staff without any mechanism to detect onset of performance degradation between visits — even if such onset produces measurable external signals, there is currently no system in place to capture and act on those signals."

### Overclaimed scalability

A single-site, 40-unit, 2-kit study cannot demonstrate "scalable, localized predictive diagnostics." It can demonstrate a *prototype approach.* The "Campus of the Future" framing adds branding without methodology. Scalability is never tested — there's no cross-site validation, no deployment at a second location, no variation in unit types/installation conditions. The claim should be downgraded to "proof-of-concept for site-specific, non-invasive AC condition monitoring."

### Unfalsifiable hypotheses

- **H2:** "Comparable performance" is subjective — no threshold, no statistical test. Unfalsifiable as written. Need a margin (e.g., within 3pp macro-F1) plus a significance test (McNemar's or paired bootstrap).
- **H4:** "Does not significantly degrade" — same problem. "Significantly" requires a defined significance test and effect-size threshold. What test? What p-value? What margin?
- **H1:** F1 ≥ 0.85 is arbitrary with no justification. For a binary task on a small, imbalanced dataset, 0.85 is optimistic AND ambiguous — which F1? Binary, macro, weighted? With 80% normal / 20% abnormal, binary-F1 on the abnormal class and weighted-F1 tell wildly different stories.

### RQ1 and RQ2 partially redundant

RQ1 asks how effective feature selection is. RQ2 asks which model classifies best. But feature selection effectiveness is measured by... classification performance. RQ1's answer is "features X and Y are selected → they produce good classification in RQ2." You're using RQ2's metric to answer RQ1. Either merge them or sharpen RQ1 to ask about *discriminatory power* (univariate analysis, effect sizes, feature importance rankings) independent of model performance.

### RQ1 scope / H2 scope mismatch

RQ1 says "dimensionality reduction techniques" (plural — PCA, UMAP, t-SNE, autoencoders?). H2 tests only PCA. Either broaden H2 to test 2-3 techniques or narrow RQ1 to match.

---

## 2. LOOPHOLES — Unaddressed Problems

### Labeling strategy (the single largest methodological hole)

Non-invasive sensors produce the *inputs.* But you need *labels* (Normal/Abnormal) to train supervised models — and those labels must come from an **independent source**, not from the same non-invasive sensors. The proposal doesn't address this at all. Options:

- **Post-hoc labeling from scheduled inspections:** At the next 3-4 month cleaning, a technician diagnoses the unit. Units found faulty are retroactively labeled abnormal for all prior visits. Problem: 3-4 month lag, and a unit could develop a fault 2 weeks before the cleaning — all its earlier visits would be labeled abnormal when they were actually normal at the time.
- **Separate diagnostic pass:** A technician does an invasive checklist inspection (not the sensors) at each visit, separate from the sensor measurements. The invasive inspection provides ground truth. This doesn't violate "non-invasive deployment" because the invasive step is only for *labeling during the study*, not for the deployed system. This is the most defensible approach and should be explicitly planned.
- **Performance benchmarking:** Compare measured cooling capacity/efficiency to manufacturer spec. Requires a reference measurement that may itself need instrumentation.

Option (b) is probably the right path, but the study needs to say so explicitly and budget for a technician at each visit.

### Data volume and class imbalance

30-40 units, most healthy. With 2 kits rotated weekly, each unit is measured maybe once every 2-5 weeks depending on throughput. Over a 9-month academic year: ~6-20 passes per unit. Of 30-40 units, how many will be abnormal? If faults occur "within 2 months of servicing," that's maybe 5-15 abnormal observations total across the entire study. Training a DNN or CNN on 5-15 positive examples is not feasible. Even RF/XGBoost will struggle.

Not addressed: **controlled fault injection** to supplement natural faults. E.g., simulating coil fouling by partially restricting airflow on a subset of units (with campus facilities' permission), or simulating a leak via controlled refrigerant reduction during a maintenance visit. This would provide a balanced dataset without waiting for natural faults. The "non-invasive" constraint applies to the *deployed sensor system*, not to the experimental setup — you can deliberately create known faults for training and then test the non-invasive sensors on them. This distinction should be made explicit.

### Vibration sensor placement vs evaporator proximity

The evaporator is in the *indoor* unit, whose only moving part is the fan motor. Most vibration signatures (compressor pressures, flow issues) originate in the *outdoor* unit. Where does the MPU6050 go?

- Indoor unit casing → you're measuring fan motor vibration, which may detect fan-side faults but is weakly coupled to evaporator health (fouling, leaks).
- Outdoor unit → closer to compressor but far from the evaporator thermodynamically. Also, "external" access to the outdoor unit is easy; "external" access to the indoor unit means a ladder and ceiling/wall access.

The vibration→spectrogram→CNN pipeline implicitly assumes the tremor carries evaporator-specific information. The proposal doesn't establish that this signal path exists. On a residential split unit, fan-induced vibration is dominated by fan motor bearing noise and blade balance — neither correlates cleanly with evaporator fouling or refrigerant leaks. H3 could be unfalsifiable for the wrong reason: if the signal doesn't carry fault information, no model, no matter how good, will learn it from 40 samples.

### CNN spectrogram training data volume

One accelerometer produces one stream per visit per unit. A spectrogram per unit per visit = ~30-40 images total (fraction abnormal). CNNs from scratch need thousands. Transfer learning (pre-trained on ImageNet) is a workaround but: (a) the "no external datasets" principle contradicts using ImageNet weights, and (b) ImageNet features for accelerometer spectrograms is a domain mismatch that may hurt more than help. This hypothesis may be untestable with available data.

### Ambient condition confounding

Units measured on a 38°C day will look "stressed" (high current draw, lower ΔT across coil) vs the same unit on a 28°C day. With sparse cross-sectional sampling, the model may learn "hot day = abnormal." Strategies not addressed:

- Collect enough data across weather conditions to learn the relationship (needs more sampling than planned)
- Normalize features by ambient conditions (requires ambient temp/humidity as model inputs, not just sensor features — BME280 covers this, good)
- Restrict measurement to a narrow ambient window (reduces data volume further)
- Include time-since-last-cleaning as a covariate (likely strong predictor — newer-cleaned units run better regardless of fault)

### Sensor kit-to-kit variation

Two portable kits means two sets of sensors. If BME280 #1 reads +0.5°C vs BME280 #2, that's a systematic bias baked into the dataset based on which kit visited which unit. Need: (a) calibration-verification protocol before deployment, (b) kit ID included as a model feature during development (to detect kit-driven bias), then excluded from final model.

### "No external datasets" — self-imposed limitation or real constraint?

The pitch says "all on-site data, no external datasets, this is a strength." It's a strength *if* you're arguing the model is site-specific and you don't need generalizability. But it eliminates:

- Transfer learning for the CNN (would help a lot)
- Pre-training on similar AC sensor datasets publicly available (there are some)
- Benchmarking your model against existing fault-detection literature
- Sanity checks on whether your features are sane

For a bachelor's thesis, site-specific framing is defensible — but the "strength" claim should be softened to "appropriate for the intended deployment context," not "a methodological advantage."

---

## 3. STRENGTHS — Where the Reframing Genuinely Improves the Original

- **Non-invasive constraint** — sharpens the contribution. The realistic deployability story is now honest: external sensors, no disassembly, feasible on a functioning campus. This is the right starting point for a working prototype.

- **Portable kits (2, not 50)** — drops hardware cost from "you will never get funding" to "this is a reasonable bachelor's thesis budget." Also makes calibration and quality control realistic with only 2 kits to manage.

- **Complementary triage framing** — abandons the indefensible "replace scheduled PM" claim. This aligns with how predictive maintenance actually works in practice (augmenting existing PM programs, not replacing them) and removes a needless target for the adviser's skepticism.

- **Binary classification scope** — correct starting point. Multi-class fault-type classification with this data volume would fail; Normal/Abnormal is achievable and still operationally useful (direct maintenance staff to flagged units first).

- **Reframed gap text** (ignoring the scalability sentence) is materially stronger than the original: the "information gap between visits" framing is a real, well-articulated gap that a reviewer can evaluate on its merits rather than being asked to take a premise on faith.

- **Conditional PMV experiment** — putting it as "conditional, if airflow sensor is developed" is the right risk-management move. It avoids over-committing to a risky sub-experiment.

---

## 4. IMPROVEMENT — Refined Research Questions and Hypotheses

### Proposed revised RQ set

**RQ1 (replaces original RQ1, focuses on discriminatory power rather than methods):**

> Which non-invasive sensor measurements (supply-return temperature differential, compressor/fan current signatures, vibration spectral features) demonstrate statistically significant discriminatory power between Normal and Abnormal AC unit conditions, as measured by univariate effect sizes and permutation importance?

Rationale: This is answerable independent of model choice. It tells a thesis panel *what the signal looks like* before the model selection question. If no univariate feature separates the classes, the whole approach is in question — better to find that early.

**RQ2 (tightened, reduced model list):**

> Among logistic regression (baseline), Random Forest, XGBoost, and RBF-SVM, which model achieves the highest macro-F1 in classifying AC unit condition using non-invasive sensor features, and does this performance exceed a majority-class baseline at p < 0.05 (McNemar's test)?

Dropped k-NN (rarely competitive on tabular at this sample size) and DNN/CNN (insufficient training data — see below).

**RQ3 (instead of PMV, addresses a real and feasible question):**

> Does incorporating delay-embedded features (time-since-last-cleaning, ambient temperature, ambient humidity) as covariates improve classification performance compared to raw sensor features alone?

Rationale: Time-since-cleaning is likely one of the strongest predictors (freshly serviced units run better). Including it explicitly answers whether the model learns the *unit's condition* vs just *how recently it was cleaned*. This is the real confound question, and it's answerable with data already being collected.

**RQ4 (replaces PMV, optional, treats vibration as exploratory):**

> Can statistical vibration features (RMS, peak amplitude, spectral kurtosis, dominant frequency) extracted from accelerometer data improve classifier performance when fused with environmental and electrical features?

Rationale: Answers whether vibration adds information without the CNN data-volume problem. If yes, future work can try CNN spectrograms with more data. If no, the vibration branch is cleanly closed out.

### Proposed revised hypotheses

**H1 (justified threshold, specified metric):**

> At least one classification model achieves macro-F1 ≥ 0.80 on the held-out test set, with 95% confidence interval lower bound exceeding the majority-class baseline macro-F1 by at least 5 percentage points.

Rationale: 0.80 is more defensible for a sparse-data prototype than 0.85. The confidence interval + baseline comparison makes it falsifiable even if the threshold is exceeded trivially.

**H2 (defined "comparable" with statistical test):**

> PCA-reduced features achieve macro-F1 within 3 percentage points of the full feature set AND show no statistically significant difference in per-sample prediction agreement (McNemar's test, p > 0.05).

Rationale: Now falsifiable. If PCA wins by more than 3pp, that's informative (PCA helps by reducing overfitting). If it loses by more than 3pp, the hypothesis is rejected (full features carry signal lost by PCA).

**H3 (replaced — vibration statistical features instead of CNN):**

> Combining vibration-derived statistical features with environmental and electrical features yields a statistically significant improvement in macro-F1 compared to using environmental and electrical features alone (paired bootstrap test, p < 0.05).

Rationale: Drops the CNN claim (untestable at this data scale) and the arbitrary 2% — replaces with a real statistical test on whether vibration adds information at all.

**H4 (drop):** The PMV hypothesis should be removed or deferred to future work. PMV is a human comfort index; using it as a machine health feature has no theoretical foundation, and the dependency on an unprovided DIY airflow sensor makes it fragile. If Kira wants to keep a "third research angle" for breadth, the time-since-cleaning covariate (RQ3 above) is more methodologically sound and addressable with existing data.

---

## Bottom Line Summary

The reframing is materially stronger than the original — non-invasive constraint, portable kits, complementary triage framing are all right calls. The three biggest issues to fix before defense:

1. **"Predictive" in the title is wrong for what the methodology does** — it's diagnostic/classification. Rename or restructure.
2. **Labeling strategy is not addressed at all** — independent ground truth (technician inspection, scheduled-cleanings-driven) needs explicit planning.
3. **Hypotheses H2 and H4 are unfalsifiable** as written — all "comparable"/"significant" thresholds need explicit margins and named statistical tests.

Minor but important: the CNN-on-spectrograms approach is very likely unworkable at 40 units of data; recommend pivoting to vibration statistical features instead. The PMV experiment conceptually doesn't connect — human comfort metrics aren't the right proxy for machine health.