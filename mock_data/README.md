# Mock H1 Data

Synthetic data for testing the H1a/H1b analysis pipeline. **This is not thesis data.**

Generated with `numpy.random.default_rng(42)`; rerunning the generator reproduces the same values.

## Folder layout

```
mock_data/
├── generate_mock_data.py
├── run_h1a_check.py
├── README.md
├── minimum/
│   ├── healthy_windows.csv
│   ├── injected_windows.csv
│   ├── trial_scores.csv
│   ├── h1a_pairs.csv
│   ├── h1a_results.csv
│   ├── summary.json
│   └── mock_data.xlsx
└── ideal/
    ├── healthy_windows.csv
    ├── injected_windows.csv
    ├── trial_scores.csv
    ├── h1a_pairs.csv
    ├── h1a_results.csv
    ├── summary.json
    └── mock_data.xlsx
```

## What each file contains

| File | One row is | Use |
|---|---|---|
| `healthy_windows.csv` | one 10-s window from a normal-condition unit | training the anomaly model |
| `injected_windows.csv` | one 10-s window from an injected unit | scoring pre/post/recovery data |
| `trial_scores.csv` | one trial, with four sensor-group scores | H1a tests; do **not** test windows |
| `h1a_pairs.csv` | one matched pre/post pair for one sensor group | inspection and Wilcoxon input |
| `h1a_results.csv` | one Wilcoxon/Holm test result | checking the expected pattern |
| `summary.json` | run counts and parameters | quick reference |
| `mock_data.xlsx` | the data tables as separate sheets | Excel users; `h1a_results` is a separate CSV |

## Scenario sizes

| | Minimum | Ideal |
|---|---:|---:|
| Healthy units | 20 | 35 |
| Injected units | 2 | 2 |
| Total units | 22 | 37 |
| Visits per healthy unit | 3 | 6 |
| Trials per visit | 10 | 10 |
| Windows per trial | 6 | 6 |
| Healthy windows (training) | 3,600 | 12,600 |
| Injected windows | 864 | 1,080 |
| Total windows | 4,464 | 13,680 |
| Healthy trials | 600 | 2,100 |
| Injection trials | 144 | 180 |
| Total trials | 744 | 2,280 |
| H1a pre/post trials | 96 | 120 |
| H1a pair rows | 192 | 240 |

## What is a pair?

A **pair** is one pre-injection trial matched with one post-injection trial from the **same unit and same fault type**.

Example for `INJ-01`, `blocked_return_air`:

| pair_id | phase | trial |
|---|---|---|
| 1 | pre | `INJ-01-blocked_return_air-pre-P01` |
| 1 | post | `INJ-01-blocked_return_air-post-P01` |
| 2 | pre | `INJ-01-blocked_return_air-pre-P02` |
| 2 | post | `INJ-01-blocked_return_air-post-P02` |

`pair_id` links the two trials. The Wilcoxon test compares the 8 (minimum) or 10 (ideal) paired differences:

```text
difference = post_score - pre_score
```

Recovery trials also carry a `pair_id`, but H1a does not use them. They are for checking whether the score returns toward baseline.

## How to run H1a on this mock data

1. Use `trial_scores.csv`.
2. Filter `unit_type == "injected"` and `phase in ["pre", "post"]`.
3. For each `unit_id` × `fault_type` × sensor group, pivot `phase` into pre/post columns by `pair_id`.
4. Run a one-sided Wilcoxon signed-rank test on `post_score > pre_score`.
5. Apply Holm correction across the **12 tests per injected unit** (4 groups × 3 faults).
6. Repeat separately for each injected unit; do not pool units.

`h1a_pairs.csv` is already in the pair-level long format, with `pre_score`, `post_score`, `difference`, and `recovery_score`.

## Run the H1a check

From the repository root:

```bash
python mock_data/run_h1a_check.py minimum
python mock_data/run_h1a_check.py ideal
```

This writes `h1a_results.csv` inside the selected scenario folder.

## Expected pattern

The generator deliberately shifts:

- **vibration** strongly after injection;
- **current/power** moderately after injection;
- **ambient** not at all;
- **airflow** for blocked/reduced faults.

So vibration and current/power should usually separate pre from post; ambient should not. The exact p-values depend on the noise, so treat this as a pipeline fixture, not a guaranteed result.

## Column dictionary

| Column | Meaning |
|---|---|
| `unit_id` | `HEALTHY-01...` or `INJ-01...` |
| `unit_type` | `healthy` or `injected` |
| `visit_id` | visit identifier |
| `trial_id` | unique 1-minute trial identifier |
| `window_index` | 0-based window number inside the trial |
| `phase` | `normal`, `pre`, `post`, or `recovery` |
| `fault_type` | `none`, `blocked_return_air`, `reduced_refrigerant`, or `misaligned_fan` |
| `pair_id` | matched pre/post pair number; blank for healthy units |
| `timestamp` | synthetic visit/trial timestamp |
| `kit_id` | `KIT-A` or `KIT-B` |
| `location` | SBM AVR, College of Engineering, or Faber Hall |
| `setpoint` | 24.0 °C |
| `ambient_temp`, `ambient_rh`, `pressure` | ambient features |
| `inlet_temp`, `outlet_temp`, `coil_temp` | temperature features |
| `current`, `voltage`, `power` | electrical features; power is derived |
| `vib_rms`, `vib_kurtosis`, `vib_peak_freq` | vibration features |
| `airflow` | airflow feature |
| `score_ambient` | mean absolute z-score of ambient features |
| `score_current_power` | mean absolute z-score of current/voltage/power |
| `score_vibration` | mean absolute z-score of vibration features |
| `score_airflow` | absolute z-score of airflow |

## Regenerate

From the repository root:

```bash
python mock_data/generate_mock_data.py
```
