# Statistical Analysis Reference — Wilcoxon Signed-Rank Test and Holm Correction

> Supporting reference for Section 3.1.7 (Statistical Analysis Samples). Covers the
> one-sided Wilcoxon signed-rank test, the Holm correction, and the family-wise error rate.

---

## Wilcoxon Signed-Rank Test

### What it is

A **non-parametric** test for **two related (paired) samples**. It asks whether the median of the differences is different from zero.

In this thesis it is used to compare **pre-injection vs post-injection trial scores** on the *same* unit and fault type, so the two values in each pair are naturally related.

It is the non-parametric alternative to the **paired t-test**, used when you cannot assume the differences are normally distributed — which matters here because the sample is tiny (9–10 pairs).

> Note: this is different from the **Wilcoxon rank-sum test (Mann–Whitney U)**, which is for two *independent* groups. Don't confuse them.

### Hypotheses

For H1a, we expect the fault to *increase* the anomaly score, so the test is **one-sided**:

$$
H_0:\ \operatorname{median}(d) \le 0
$$

$$
H_1:\ \operatorname{median}(d) > 0
$$

where $d_i = S_{\text{post},i} - S_{\text{pre},i}$.

### Assumptions

1. The data are **paired** (one pre and one post for the same unit, fault, and trial index).
2. The differences are **independent** across pairs.
3. The differences are measured on an **interval or ordinal** scale (so we can rank them).
4. The distribution of differences is **symmetric** about its median. (If it isn't symmetric, use the **sign test** instead.)

### Step-by-step procedure

1. Compute differences: $d_i = x_i - y_i$.
2. Drop any $d_i = 0$ (zeros) and reduce $n$ accordingly.
3. Rank the **absolute** differences $|d_i|$ from smallest (1) to largest (n). Ties get the average of the ranks they span.
4. Sum the ranks of the positive differences → $W_+$, and of the negative differences → $W_-$.
5. Under $H_0$, the ranks should split evenly, so both are about $n(n+1)/4$. A big imbalance is evidence against $H_0$.
6. Compute the test statistic and p-value.

For a **one-sided test in the positive direction**, a small $W_-$ (most differences positive) is the signal. Equivalently, $p = P(W_+ \ge \text{observed } W_+)$.

### The smallest possible p-value

Under $H_0$, every difference is a coin flip (positive/negative). With $n$ nonzero pairs there are $2^n$ equally likely sign patterns, and the most extreme pattern (all one sign) has probability:

$$
p_{\min} = \frac{1}{2^n}
$$

This is why $n$ matters so much for H1a.

### Effect size

The **matched-pairs rank-biserial correlation**:

$$
r = \frac{W_+ - W_-}{W_+ + W_-}
$$

It ranges from −1 to +1 and is the non-parametric analog of a correlation/effect size, independent of sample size.

---

## Holm Correction

### Why multiple tests need a correction

If you run $m$ tests at $\alpha = 0.05$, the chance of finding **at least one** false positive grows quickly. That's the **family-wise error rate** problem (see below).

Holm correction (a.k.a. **Holm–Bonferroni**) is a way to keep that chance at or below $\alpha$.

### How it works (step-down)

1. Sort your $m$ p-values from smallest to largest:

$$
p_{(1)} \le p_{(2)} \le \dots \le p_{(m)}
$$

2. Compare each $p_{(k)}$ to the threshold:

$$
\frac{\alpha}{m - k + 1}
$$

3. Reject hypotheses as long as the p-value stays at or below its threshold. The **first** time a p-value exceeds its threshold, stop — reject everything before it, fail to reject it and everything after it.

The thresholds get **more relaxed** as you go down the list: the smallest p has the hardest bar, the largest has the easiest.

### Worked example: the 15 H1a tests

With $m = 15$ and $\alpha = 0.05$:

| Rank $k$ | Holm threshold $\alpha/(m-k+1)$ |
|---:|---:|
| 1 (smallest p) | 0.05 / 15 = **0.0033** |
| 2 | 0.05 / 14 = 0.0036 |
| 3 | 0.05 / 13 = 0.0038 |
| 4 | 0.05 / 12 = 0.0042 |
| … | … |
| 14 | 0.05 / 2 = 0.0250 |
| 15 (largest p) | 0.05 / 1 = **0.0500** |

So the single hardest cutoff — the one everyone quotes — is **0.0033**, applied to the *smallest* p-value.

### Holm vs Bonferroni vs Benjamini–Hochberg

| Method | Controls | Approach | Power |
|---|---|---|---|
| Bonferroni | FWER | compare every p to $\alpha/m$ | least powerful |
| **Holm** | FWER | step-down, $\alpha/(m-k+1)$ | more powerful than Bonferroni |
| Benjamini–Hochberg | FDR | step-up | most powerful (but allows some false discoveries) |

Holm is almost always preferable to Bonferroni: it's equally conservative on the first test but relaxes as it goes, so it finds more true effects.

---

## Family-Wise Error Rate (FWER)

### Definition

> The **family-wise error rate** is the probability of making **at least one** Type I error (false positive) across a whole **family** of tests.

In H1a, the "family" is the **15 tests** (5 sensor groups × 3 fault types) run on one injected unit.

### Why it blows up

If you run $m$ independent tests, each at level $\alpha$, the chance of at least one false positive is:

$$
\mathrm{FWER} = 1 - (1 - \alpha)^m
$$

For $m = 15$ and $\alpha = 0.05$:

$$
1 - 0.95^{15} = 1 - 0.4633 = 0.5367 \approx 54\%
$$

So without correction, running 15 tests gives you a **better than half chance** of claiming at least one "significant" result that is actually just noise.

That is exactly why H1a applies **Holm correction** across its 15 tests — to force $\mathrm{FWER} \le 0.05$.

### FWER vs FDR

- **FWER** — "at least one false positive anywhere." Strict, good when any single false claim is costly.
- **FDR (false discovery rate)** — "what fraction of my discoveries are false." More lenient, used in exploratory work with many tests.

For H1a's confirmatory gate, FWER control (Holm) is the appropriate choice.

---

## How Many Tests Are There?

### The H1a family

H1a is one Wilcoxon signed-rank test per **sensor group × fault type**.

- 5 sensor groups: ambient, thermal, current, vibration, airflow
- 3 fault types: blocked return air, reduced refrigerant, misaligned fan

That gives:

$$
5 \times 3 = 15 \text{ tests per injected unit}
$$

The full set of 15 tests per unit is:

| # | Sensor group | Fault type |
|---:|---|---|
| 1 | Ambient | Blocked return air |
| 2 | Ambient | Reduced refrigerant |
| 3 | Ambient | Misaligned fan |
| 4 | Thermal | Blocked return air |
| 5 | Thermal | Reduced refrigerant |
| 6 | Thermal | Misaligned fan |
| 7 | Current | Blocked return air |
| 8 | Current | Reduced refrigerant |
| 9 | Current | Misaligned fan |
| 10 | Vibration | Blocked return air |
| 11 | Vibration | Reduced refrigerant |
| 12 | Vibration | Misaligned fan |
| 13 | Airflow | Blocked return air |
| 14 | Airflow | Reduced refrigerant |
| 15 | Airflow | Misaligned fan |

### Across injected units

The study uses **2 injected units**. Because units are analyzed separately and never pooled, the Holm correction is applied **within each unit**, not across the two together.

| Scope | Tests | Holm family |
|---|---:|---|
| Per injected unit | 15 | 15 (corrected together) |
| Across 2 injected units | 30 | 2 families of 15 each |

So the "15 tests" in the Holm cutoff is the **per-unit** family; the total across the study is **30 H1a tests**, split into two independent Holm families.

### Tests across the whole study (for reference)

H1a is the only confirmatory gate that uses a 15-test Holm family. The other hypotheses use their own tests:

| Hypothesis | Test(s) | Count |
|---|---|---|
| H1a | One-sided Wilcoxon per group × fault | 15 per unit |
| H1b | Paired bootstrap on the vibration gap | per fault type/unit |
| H2a | Wilcoxon per model × fault + TPR/FPR/AUC | 12 per unit + metrics |
| H2b | ΔTPR + McNemar (full vs PCA) | 1 |
| H3 | ΔTPR (PMV vs raw) | 1 (conditional) |
| H4a | ΔTPR/AUC + McNemar (LOUO) | 1 |
| H4b | Spearman + ANOVA for confounds | 5 |

---

## How This Maps Back to H1a

1. Each sensor group × fault type = one Wilcoxon signed-rank test on its pre/post trial-score pairs.
2. There are 5 × 3 = **15 tests** per injected unit.
3. Apply **Holm correction** across those 15, so the strictest cutoff is $0.05/15 = 0.0033$.
4. The smallest exact one-sided Wilcoxon p is $1/2^n$, so **at least 9 pairs** are needed for that p (0.0020) to beat 0.0033.
5. With only **8 pairs**, the smallest possible p is 0.0039, which cannot clear 0.0033 — so H1a would be **exploratory, not confirmatory**.

---

## Resources

- Wilcoxon signed-rank test — Wikipedia: https://en.wikipedia.org/wiki/Wilcoxon_signed-rank_test
- Holm–Bonferroni method — Wikipedia: https://en.wikipedia.org/wiki/Holm%E2%80%93Bonferroni_method
- Family-wise error rate — Wikipedia: https://en.wikipedia.org/wiki/Family-wise_error_rate
- Multiple comparisons problem — Wikipedia: https://en.wikipedia.org/wiki/Multiple_comparisons_problem
- Wilcoxon signed-rank test tutorial — Real Statistics: https://real-statistics.com/non-parametric-tests/wilcoxon-signed-ranks-test/
- Laerd Statistics (paired Wilcoxon): https://statistics.laerd.com/spss-tutorials/wilcoxon-signed-rank-test-using-spss-statistics.php
- Python: `scipy.stats.wilcoxon`, `statsmodels.stats.multitest.multipletests(method='holm')`
- R: `wilcox.test(...)`, `p.adjust(p, method = "holm")`

References (books):

- Conover, W. J. (1999). *Practical Nonparametric Statistics* (3rd ed.). Wiley.
- Hollander, M., & Wolfe, D. A. (1999). *Nonparametric Statistical Methods* (2nd ed.). Wiley.
