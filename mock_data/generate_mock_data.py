"""Generate synthetic H1 mock data for pipeline testing.

This is NOT thesis data. It is a reproducible fixture with known post-injection
shifts so the H1a pairing, aggregation, and Wilcoxon/Holm code can be tested.

Run from the repository root:
    python mock_data/generate_mock_data.py
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent
SEED = 42

SCENARIOS = {
    "minimum": {
        "n_healthy": 20,
        "visits": 3,
        "trials_per_visit": 10,
        "windows_per_trial": 6,
        "pairs_per_fault": 8,
    },
    "ideal": {
        "n_healthy": 35,
        "visits": 6,
        "trials_per_visit": 10,
        "windows_per_trial": 6,
        "pairs_per_fault": 10,
    },
}

FAULTS = [
    "blocked_return_air",
    "reduced_refrigerant",
    "misaligned_fan",
]
PHASES = ["pre", "post", "recovery"]
LOCATIONS = ["SBM AVR", "College of Engineering", "Faber Hall"]

# Baseline distributions: (mean, standard deviation)
FEATURE_SPECS = {
    "ambient_temp": (27.0, 1.5),
    "ambient_rh": (70.0, 8.0),
    "pressure": (1013.0, 3.0),
    "inlet_temp": (27.0, 1.2),
    "outlet_temp": (16.0, 1.5),
    "coil_temp": (10.0, 2.0),
    "current": (5.0, 0.4),
    "voltage": (230.0, 3.0),
    "vib_rms": (0.05, 0.01),
    "vib_kurtosis": (3.0, 0.3),
    "vib_peak_freq": (25.0, 3.0),
    "airflow": (2.5, 0.3),
}
FEATURE_COLS = list(FEATURE_SPECS) + ["power"]

# Post-injection shifts. Ambient is deliberately left unchanged.
EFFECTS = {
    "blocked_return_air": {
        "outlet_temp": 3.0,
        "current": 0.80,
        "vib_rms": 0.030,
        "vib_kurtosis": 0.50,
        "airflow": -1.00,
    },
    "reduced_refrigerant": {
        "outlet_temp": 4.0,
        "coil_temp": 3.0,
        "current": 1.00,
        "vib_rms": 0.020,
        "airflow": -0.50,
    },
    "misaligned_fan": {
        "vib_rms": 0.050,
        "vib_kurtosis": 1.00,
        "vib_peak_freq": 8.0,
        "current": 0.40,
        "airflow": -0.20,
    },
}

GROUP_SCORE_COLS = [
    "score_ambient",
    "score_current_power",
    "score_vibration",
    "score_airflow",
]

GROUP_MAP = {
    "ambient": "score_ambient",
    "current_power": "score_current_power",
    "vibration": "score_vibration",
    "airflow": "score_airflow",
}


def make_offsets(rng: np.random.Generator, scale: float = 0.15) -> dict[str, float]:
    return {feature: rng.normal(0, scale) for feature in FEATURE_SPECS}


def make_noise(rng: np.random.Generator, scale: float = 0.3) -> dict[str, float]:
    return {feature: rng.normal(0, scale) for feature in FEATURE_SPECS}


def make_window(
    rng: np.random.Generator,
    unit_offset: dict[str, float],
    visit_offset: dict[str, float],
    trial_offset: dict[str, float],
) -> dict[str, float]:
    x: dict[str, float] = {}
    for feature, (mean, sd) in FEATURE_SPECS.items():
        x[feature] = mean + sd * (
            unit_offset[feature]
            + visit_offset[feature]
            + trial_offset[feature]
            + rng.normal(0, 1)
        )

    # Power is derived from current and voltage, not generated independently.
    x["power"] = x["current"] * x["voltage"] * 0.9 + rng.normal(0, 15)
    return x


def group_score(frame: pd.DataFrame, columns: list[str], stats: pd.DataFrame) -> pd.Series:
    z = (frame[columns] - stats.loc[columns, "mean"]) / stats.loc[columns, "std"]
    return z.abs().mean(axis=1)


def make_trial_tables(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    score_cols = GROUP_SCORE_COLS
    group_cols = [
        "unit_id",
        "unit_type",
        "visit_id",
        "trial_id",
        "phase",
        "fault_type",
        "pair_id",
        "timestamp",
        "kit_id",
        "location",
        "setpoint",
    ]

    trial = (
        df.groupby(group_cols, dropna=False)[score_cols]
        .median()
        .reset_index()
    )

    injected = trial[trial["unit_type"] == "injected"].copy()
    pivoted = injected.pivot_table(
        index=["unit_id", "fault_type", "pair_id"],
        columns="phase",
        values=score_cols,
        aggfunc="first",
    )

    pair_rows = []
    for (unit_id, fault_type, pair_id), row in pivoted.iterrows():
        for group, score_col in GROUP_MAP.items():
            pre = float(row[(score_col, "pre")])
            post = float(row[(score_col, "post")])
            recovery = float(row[(score_col, "recovery")])
            pair_rows.append(
                {
                    "unit_id": unit_id,
                    "fault_type": fault_type,
                    "pair_id": int(pair_id),
                    "sensor_group": group,
                    "pre_score": round(pre, 4),
                    "post_score": round(post, 4),
                    "difference": round(post - pre, 4),
                    "recovery_score": round(recovery, 4),
                }
            )

    pairs = pd.DataFrame(pair_rows)
    return trial, pairs


def generate_scenario(name: str, config: dict[str, int]) -> dict[str, object]:
    rng = np.random.default_rng(SEED)
    base_time = pd.Timestamp("2026-01-05")

    n_healthy = config["n_healthy"]
    visits = config["visits"]
    trials_per_visit = config["trials_per_visit"]
    windows_per_trial = config["windows_per_trial"]
    pairs_per_fault = config["pairs_per_fault"]

    rows: list[dict[str, object]] = []

    # Healthy units: normal-condition training data.
    for i in range(n_healthy):
        unit_id = f"HEALTHY-{i + 1:02d}"
        unit_offset = make_offsets(rng)
        location = LOCATIONS[i % len(LOCATIONS)]
        kit_id = "KIT-A" if i % 2 == 0 else "KIT-B"

        for visit in range(visits):
            visit_offset = make_noise(rng, 0.30)
            visit_id = f"{unit_id}-V{visit + 1:02d}"

            for trial_num in range(trials_per_visit):
                trial_offset = make_noise(rng, 0.50)
                trial_id = f"{visit_id}-T{trial_num + 1:02d}"
                timestamp = base_time + pd.Timedelta(
                    days=visit * 7,
                    minutes=trial_num * 2,
                )

                for window_index in range(windows_per_trial):
                    x = make_window(rng, unit_offset, visit_offset, trial_offset)
                    rows.append(
                        {
                            "unit_id": unit_id,
                            "unit_type": "healthy",
                            "visit_id": visit_id,
                            "trial_id": trial_id,
                            "window_index": window_index,
                            "phase": "normal",
                            "fault_type": "none",
                            "pair_id": np.nan,
                            "timestamp": timestamp,
                            "kit_id": kit_id,
                            "location": location,
                            "setpoint": 24.0,
                            **x,
                        }
                    )

    # Injected units: pre/post/recovery fault-injection data.
    for i in range(2):
        unit_id = f"INJ-{i + 1:02d}"
        unit_offset = make_offsets(rng)
        location = LOCATIONS[i % len(LOCATIONS)]
        kit_id = "KIT-A" if i % 2 == 0 else "KIT-B"

        for fault_index, fault in enumerate(FAULTS):
            visit_id = f"{unit_id}-{fault}"

            for pair_id in range(1, pairs_per_fault + 1):
                # Shared across phases so pre/post trials are genuinely paired.
                # Lower injected noise keeps the known effects visible in the fixture.
                pair_offset = make_noise(rng, 0.10)

                for phase_index, phase in enumerate(PHASES):
                    phase_offset = make_noise(rng, 0.10)
                    trial_id = f"{visit_id}-{phase}-P{pair_id:02d}"
                    timestamp = (
                        base_time
                        + pd.Timedelta(
                            days=fault_index * 3,
                            hours=phase_index * 3,
                            minutes=pair_id * 10,
                        )
                    )

                    if phase == "post":
                        effect = EFFECTS[fault]
                    elif phase == "recovery":
                        effect = {k: 0.10 * v for k, v in EFFECTS[fault].items()}
                    else:
                        effect = {}

                    for window_index in range(windows_per_trial):
                        x = make_window(rng, unit_offset, pair_offset, phase_offset)
                        for feature, delta in effect.items():
                            x[feature] += delta

                        # Recompute power after current changes.
                        x["power"] = x["current"] * x["voltage"] * 0.9 + rng.normal(0, 15)

                        rows.append(
                            {
                                "unit_id": unit_id,
                                "unit_type": "injected",
                                "visit_id": visit_id,
                                "trial_id": trial_id,
                                "window_index": window_index,
                                "phase": phase,
                                "fault_type": fault,
                                "pair_id": pair_id,
                                "timestamp": timestamp,
                                "kit_id": kit_id,
                                "location": location,
                                "setpoint": 24.0,
                                **x,
                            }
                        )

    df = pd.DataFrame(rows)
    healthy = df[df["unit_type"] == "healthy"].copy()
    injected = df[df["unit_type"] == "injected"].copy()

    # Baseline statistics from healthy windows only.
    stats = healthy[FEATURE_COLS].agg(["mean", "std"]).T

    df["score_ambient"] = group_score(
        df, ["ambient_temp", "ambient_rh", "pressure"], stats
    )
    df["score_current_power"] = group_score(
        df, ["current", "voltage", "power"], stats
    )
    df["score_vibration"] = group_score(
        df, ["vib_rms", "vib_kurtosis", "vib_peak_freq"], stats
    )
    df["score_airflow"] = group_score(df, ["airflow"], stats)

    trial, pairs = make_trial_tables(df)

    scenario_dir = ROOT / name
    scenario_dir.mkdir(parents=True, exist_ok=True)

    healthy.to_csv(scenario_dir / "healthy_windows.csv", index=False)
    injected.to_csv(scenario_dir / "injected_windows.csv", index=False)
    trial.to_csv(scenario_dir / "trial_scores.csv", index=False)
    pairs.to_csv(scenario_dir / "h1a_pairs.csv", index=False)

    summary = {
        "scenario": name,
        "n_healthy_units": n_healthy,
        "n_injected_units": 2,
        "n_total_units": n_healthy + 2,
        "visits_per_unit": visits,
        "trials_per_visit": trials_per_visit,
        "windows_per_trial": windows_per_trial,
        "pairs_per_fault": pairs_per_fault,
        "healthy_windows": int(len(healthy)),
        "injected_windows": int(len(injected)),
        "total_windows": int(len(df)),
        "healthy_trials": int(healthy["trial_id"].nunique()),
        "injection_trials": int(injected["trial_id"].nunique()),
        "total_trials": int(df["trial_id"].nunique()),
        "h1a_prepost_trials": int(2 * 3 * 2 * pairs_per_fault),
        "h1a_pair_rows": int(len(pairs)),
        "h1a_tests_total": int(2 * 3 * 4),
        "h1a_tests_per_unit": 12,
    }

    (scenario_dir / "summary.json").write_text(
        json.dumps(summary, indent=2), encoding="utf-8"
    )

    with pd.ExcelWriter(scenario_dir / "mock_data.xlsx", engine="openpyxl") as writer:
        pd.DataFrame([summary]).to_excel(writer, sheet_name="summary", index=False)
        healthy.to_excel(writer, sheet_name="healthy_windows", index=False)
        injected.to_excel(writer, sheet_name="injected_windows", index=False)
        trial.to_excel(writer, sheet_name="trial_scores", index=False)
        pairs.to_excel(writer, sheet_name="h1a_pairs", index=False)

    return summary


def write_readme(summaries: dict[str, dict[str, object]]) -> None:
    min_summary = summaries["minimum"]
    ideal_summary = summaries["ideal"]

    readme = f"""# Mock H1 Data

Synthetic data for testing the H1a/H1b analysis pipeline. **This is not thesis data.**

Generated with `numpy.random.default_rng({SEED})`; rerunning the generator reproduces the same values.

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
| Healthy units | {min_summary["n_healthy_units"]} | {ideal_summary["n_healthy_units"]} |
| Injected units | {min_summary["n_injected_units"]} | {ideal_summary["n_injected_units"]} |
| Total units | {min_summary["n_total_units"]} | {ideal_summary["n_total_units"]} |
| Visits per healthy unit | {min_summary["visits_per_unit"]} | {ideal_summary["visits_per_unit"]} |
| Trials per visit | {min_summary["trials_per_visit"]} | {ideal_summary["trials_per_visit"]} |
| Windows per trial | {min_summary["windows_per_trial"]} | {ideal_summary["windows_per_trial"]} |
| Healthy windows (training) | {min_summary["healthy_windows"]:,} | {ideal_summary["healthy_windows"]:,} |
| Injected windows | {min_summary["injected_windows"]:,} | {ideal_summary["injected_windows"]:,} |
| Total windows | {min_summary["total_windows"]:,} | {ideal_summary["total_windows"]:,} |
| Healthy trials | {min_summary["healthy_trials"]:,} | {ideal_summary["healthy_trials"]:,} |
| Injection trials | {min_summary["injection_trials"]:,} | {ideal_summary["injection_trials"]:,} |
| Total trials | {min_summary["total_trials"]:,} | {ideal_summary["total_trials"]:,} |
| H1a pre/post trials | {min_summary["h1a_prepost_trials"]} | {ideal_summary["h1a_prepost_trials"]} |
| H1a pair rows | {min_summary["h1a_pair_rows"]} | {ideal_summary["h1a_pair_rows"]} |

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
"""
    (ROOT / "README.md").write_text(readme, encoding="utf-8")


def main() -> None:
    summaries: dict[str, dict[str, object]] = {}
    for name, config in SCENARIOS.items():
        summary = generate_scenario(name, config)
        summaries[name] = summary
        print(
            f"{name:8s} | "
            f"windows={summary['total_windows']:,} | "
            f"trials={summary['total_trials']:,} | "
            f"H1a pre/post trials={summary['h1a_prepost_trials']}"
        )

    write_readme(summaries)
    print(f"\nWrote mock data to {ROOT}")


if __name__ == "__main__":
    main()
