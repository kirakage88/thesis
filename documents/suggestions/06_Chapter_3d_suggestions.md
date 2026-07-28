# Chapter III (Part 4): Evaluation, Deployment & Workflow — Suggestions & Loopholes

## Loopholes

### L1. Missing Post-Hoc Test After Friedman Test

The Friedman Test determines whether **at least one model differs** from the others. If the null hypothesis is rejected, it doesn't tell you **which** models differ. A **post-hoc test** is required:
- **Nemenyi test** — compares all pairs of models, the standard post-hoc for Friedman.
- **Wilcoxon signed-rank with Bonferroni correction** — for pairwise comparisons.

Without a post-hoc test, you can say "models differ" but not "Model A is significantly better than Model B."

### L2. No Justification for 30 Subsets

The test split is grouped into **30 subsets** for cross-validation across models. Why 30? No statistical justification is given. Relevant considerations:
- 30 is the conventional threshold for the Central Limit Theorem — but this applies to sample sizes, not subset counts.
- With a small test set (20% of the total 6-month dataset), 30 subsets may be very small (potentially only a few readings each).
- Minimum subset size affects the stability of per-subset accuracy estimates.

### L3. No Statistical Power Analysis

The methodology describes hypothesis testing (Friedman test) but doesn't conduct a **power analysis**:
- What effect size is expected?
- Is the sample size (number of test readings) sufficient to detect a meaningful difference between models?
- What's the risk of Type II error (failing to detect a real difference)?

### L4. No Model Deployment Reliability Considerations

The Streamlit + SQLite + Watchdog pipeline is described optimistically. Missing considerations:
- **Failed predictions:** What happens if `model.predict()` throws an error (malformed input, NaN values)?
- **Model confidence threshold:** Does every prediction trigger an alert? Or only predictions with probability > 0.7? False alarms will desensitize maintenance staff.
- **Alert escalation:** How many consecutive "Abnormal" predictions before a maintenance action is triggered? One abnormal reading could be noise.
- **Model drift detection:** How do you know if the deployed model's performance is degrading over time?

### L5. No Security Considerations

- The Streamlit dashboard has no authentication — anyone on the network can view/modify AC unit data.
- SQLite database has no encryption.
- ESP-NOW communication is unencrypted (`peerInfo.encrypt = false` in the codebase).
- Supabase credentials are hardcoded in firmware (visible in the repo).

### S6. No Model Retraining Strategy

The deployment is one-shot: train once, deploy, and run predictions forever. But:
- New data accumulates over the 6-month period.
- Sensor drift may occur.
- Seasonal changes affect AC behavior.

**Missing:** A plan for periodic retraining, online learning, or at least a scheduled model update cycle.

### L7. Watchdog Architecture Has a Race Condition Risk

The watchdog triggers on file creation in `02_Data/raw/`. If the Ingest Server is still writing the file when watchdog fires, the prediction pipeline may read an incomplete CSV.

**Fix:** Trigger on file **close/write-complete** events, or use a staging directory + atomic move.

### L8. No Discussion of Inference Latency

For real-time deployment, inference latency matters:
- How long does preprocessing take per reading?
- How long does model prediction take?
- Is there a delay between sensor reading and dashboard update?
- What's the end-to-end latency target?

## Suggestions for Improvement

### S1. Add Post-Hoc Nemenyi Test
After Friedman test, add:
- Nemenyi test for pairwise model comparison.
- Critical difference (CD) diagram — a visual ranking of models showing which are statistically significantly different.
- Reference: Demsar (2006), "Statistical Comparisons of Classifiers over Multiple Data Sets."

### S2. Justify the Number of Subsets
Either:
- Justify 30 with a reference or statistical reasoning.
- Or use the 5-fold CV results directly for Friedman test (each fold = one "subset"), giving 5 subsets per model comparison. This is the standard approach in ML.

### S3. Add Alert Threshold Logic
Define:
- **Prediction confidence threshold:** Only flag "Abnormal" if model probability > 0.7 (configurable).
- **Temporal smoothing:** Require N consecutive abnormal predictions before alerting (e.g., N=3).
- **Alert priority levels:** Warning (probability 0.5–0.7), Alert (0.7–0.85), Critical (>0.85).

### S4. Add Error Handling in the Inference Pipeline
Describe:
- Input validation (check for NaN, out-of-range values, correct column count).
- Fallback behavior (if prediction fails, log error, skip file, alert administrator).
- Dead-letter queue for failed predictions.

### S5. Add Authentication to the Dashboard
- Streamlit supports `st.experimental_get_query_params` for basic auth, or use `streamlit-authenticator` library.
- At minimum, add HTTP Basic Auth via Streamlit's settings or a reverse proxy (nginx).

### S6. Add Model Retraining Plan
Describe:
- **Scheduled retraining:** Retrain monthly on accumulated data.
- **Triggered retraining:** Retrain when prediction confidence drops below threshold.
- **A/B testing:** Run new model in shadow mode alongside deployed model before promotion.

### S7. Address the Watchdog Race Condition
Change the file event trigger to:
- Watch for `FILE_CLOSED` events, not `FILE_CREATED`.
- Or use a staging directory: Ingest Server writes to `raw/.staging/`, then atomically moves to `raw/` when complete. Watchdog monitors `raw/` only.