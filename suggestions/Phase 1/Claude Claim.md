# Claude Recommendation
### Methodology Decision: Supervised Classification vs. Unsupervised Anomaly Detection
**Thesis:** Development of a Predictive Maintenance Model for Coiled Evaporators in Split-Type Air Conditioning Systems

---

## Recommendation: Option B (Unsupervised Anomaly Detection), with a hybrid validation layer

### Why B over A

The deciding factor is what the data actually supports, not which approach is more "standard." With only 13 documented problem units out of 2,599 campus-wide, and only 30–40 units actually being instrumented, you're very likely to end up with **0–2 confirmed abnormal units in your instrumented subset** over a 6-month window. That's not "severe class imbalance" — that's an effective absence of a positive class. Supervised classification with that few positive examples doesn't produce a weak model; it produces a model you cannot validate at all, because your test set won't contain enough abnormal cases to compute a meaningful precision/recall/F1 with any statistical confidence. A single misclassified unit swings your recall by 50–100%.

The proposed labeling strategy compounds this: a technician's weekly "Normal/Degraded" visual call is a *subjective proxy label*, not ground truth, especially given the non-invasive constraint (no evaporator access) already limits what any human or sensor can actually observe. You'd be training a supervised model to reproduce a noisy, low-base-rate, subjectively-labeled signal — which is a much harder and less defensible target than it first appears.

Unsupervised anomaly detection sidesteps this cleanly: it doesn't need the rare class to be well-represented, it needs the *normal* operating envelope to be well-represented — which you have in abundance (30–40 units × weekly visits × 6 months = plenty of "normal" data even if faults are rare). This is also the more honest framing given your actual constraints: you are not proving "we can classify Normal vs Abnormal with 85% F1," you're proving "we can characterize normal operation precisely enough to flag meaningful deviations" — which is a claim your data can actually support.

### Strongest argument for Option A (the one not recommended)

The strongest case for supervised classification is **interpretability and stakeholder buy-in**. A maintenance manager can act on "this unit is predicted Abnormal" immediately; they cannot act on "this unit has an anomaly score of 0.82" without translation. HVAC PdM literature overwhelmingly uses supervised classification precisely because the output maps directly onto an operational decision (send a technician or don't). If your adviser or defense panel is used to seeing accuracy/F1 tables as "real" ML results, an anomaly-score-based output will read as less rigorous or less finished, even if it's the more statistically honest choice given your label scarcity. There's also real value in H3 (CNN spectrogram vs. tabular) being a supervised-style comparison — anomaly detection makes "does the CNN help" a fuzzier question to answer cleanly.

That's a real cost, and a legitimate reason a committee might push back on Option B.

### Validation strategy for Option B

Since "how do you prove it works without labels" is the obvious defense-day question, build validation in layers rather than relying on a single metric:

1. **Retrospective validation against maintenance logs.** Treat the 13 campus-wide known-issue units as a *held-out sanity check*, not a training signal. If any are among your instrumented 30–40, report anomaly scores for those units leading up to their documented fault date. A plot showing anomaly score rising before a known documented issue is compelling, honest evidence — and directly tests the core value proposition (catching degradation *before* the scheduled cleaning reveals it).

2. **Injected/synthetic fault validation.** Since real fault data will be sparse, artificially perturb held-out sensor readings (e.g., simulate a partially blocked coil by shifting the temp differential, simulate compressor strain by injecting current draw anomalies) and confirm the model flags these as anomalous. This is standard practice in unsupervised PdM literature specifically *because* real fault data is rare.

3. **Agreement with technician spot-checks (as external validation, not as labels).** Keep the technician inspection, but reframe its role: instead of "ground truth for training," it becomes an independent human judgment correlated against model anomaly scores after the fact. Report agreement rate as supporting evidence — this also protects against circularity criticism.

4. **Time-since-last-cleaning as a confound control.** Since this is a strong predictor available from logs, use it explicitly to distinguish "anomalous because degrading" from "anomalous because overdue for scheduled cleaning" — report anomaly scores stratified by time-since-cleaning to show the model isn't just rediscovering the maintenance schedule.

5. **Stability/consistency check.** A unit that's genuinely degrading should show a rising, persistent anomaly signal across nearby time points — not single-visit noise spikes, which are more likely sensor artifacts or transient conditions like a hot day.

Together, these give multiple independent lines of evidence rather than a single (currently unattainable) clean F1 score — a stronger defense posture than a supervised model whose F1 is computed on 1–2 positive examples.

### If Option A is used anyway — addressing the bottleneck and imbalance

- **Synthetic/injected fault augmentation** (as above) to artificially create a larger, more balanced "Abnormal" training set, clearly labeled as synthetic in the methodology, with real data reserved entirely for testing.
- **Cost-sensitive learning / class weighting** (weighted loss functions, SMOTE-family oversampling only on the training fold, never on the test fold) to prevent the classifier from trivially predicting "Normal" for everything.
- **Report per-class metrics, not aggregate accuracy**, and be explicit that recall on the Abnormal class is the metric that matters operationally.
- **Reduce the labeling bottleneck** by narrowing technician inspection to units already flagged by a lightweight rule-based prefilter (e.g., threshold-based alerts on temp differential or current draw), rather than inspecting all 30–40 units weekly.

### Which option is easier to DEFEND, independent of which is "better"

**Option A is easier to defend in the room**, even though Option B is the more defensible *methodology* given the actual data constraints. A thesis committee — especially one already skeptical of PdM replacing preventive maintenance — will find "we trained a classifier and got X% F1" more legible and easier to interrogate using familiar rubrics (confusion matrix, precision/recall, comparison table across 5 models) than "we built an anomaly detector and validated it via score trajectories and synthetic fault injection," which requires the panel to accept a less familiar evaluation paradigm on the spot.

The risk with A: the *moment* someone asks "how many actual abnormal units did you have in your test set," the honest answer (likely single digits or zero) undermines the entire F1 table — a much worse moment than proactively saying "given documented base rates, standard classification metrics would be statistically meaningless here, so we used anomaly detection with these validation layers instead." Framed *that way*, upfront, in the methodology section — as a data-driven choice rather than a shortcut — Option B becomes not just defensible but a demonstration of methodological maturity.

**Bottom line:** lead with B, but explicitly frame the choice in the methodology chapter as a direct response to the label scarcity problem — walk the committee through the 13-in-2,599 base rate before introducing the model choice, so the anomaly-detection framing lands as the obviously correct response to the data, not an evasion of "real" classification.
