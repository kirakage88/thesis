"""Run the H1a paired Wilcoxon check on the mock data.

Usage:
    python mock_data/run_h1a_check.py minimum
    python mock_data/run_h1a_check.py ideal
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import wilcoxon

SCENARIO = sys.argv[1] if len(sys.argv) > 1 else "minimum"
BASE = Path(__file__).resolve().parent / SCENARIO
PAIRS_PATH = BASE / "h1a_pairs.csv"
OUT_PATH = BASE / "h1a_results.csv"

GROUPS = ["ambient", "current_power", "vibration", "airflow"]


def holm_adjust(pvalues: list[float]) -> np.ndarray:
    pvalues_array = np.asarray(pvalues, dtype=float)
    m = len(pvalues_array)
    order = np.argsort(pvalues_array)
    adjusted = np.empty(m)
    previous = 0.0

    for rank, index in enumerate(order):
        value = min(1.0, (m - rank) * pvalues_array[index])
        value = max(value, previous)
        adjusted[index] = value
        previous = value

    return adjusted


def main() -> None:
    pairs = pd.read_csv(PAIRS_PATH)
    results = []

    for unit_id in sorted(pairs["unit_id"].unique()):
        unit_tests = []

        for fault_type in sorted(pairs["fault_type"].unique()):
            for group in GROUPS:
                subset = pairs[
                    (pairs["unit_id"] == unit_id)
                    & (pairs["fault_type"] == fault_type)
                    & (pairs["sensor_group"] == group)
                ].sort_values("pair_id")

                pre = subset["pre_score"].to_numpy()
                post = subset["post_score"].to_numpy()

                if len(pre) != len(post) or len(pre) < 1:
                    raise ValueError(
                        f"Invalid pair data for {unit_id}, {fault_type}, {group}"
                    )

                stat, p_value = wilcoxon(
                    post,
                    pre,
                    alternative="greater",
                    zero_method="wilcox",
                )

                unit_tests.append(
                    {
                        "unit_id": unit_id,
                        "fault_type": fault_type,
                        "sensor_group": group,
                        "n_pairs": len(pre),
                        "pre_mean": round(float(pre.mean()), 4),
                        "post_mean": round(float(post.mean()), 4),
                        "median_difference": round(float(np.median(post - pre)), 4),
                        "statistic": float(stat),
                        "p_value": float(p_value),
                    }
                )

        adjusted = holm_adjust([test["p_value"] for test in unit_tests])
        for test, p_adjusted in zip(unit_tests, adjusted):
            test["holm_p_value"] = float(p_adjusted)
            test["significant"] = bool(p_adjusted < 0.05)
            results.append(test)

    result_df = pd.DataFrame(results)
    result_df.to_csv(OUT_PATH, index=False)

    print(f"Scenario: {SCENARIO}")
    print(f"Saved: {OUT_PATH}\n")
    print(
        result_df[
            [
                "unit_id",
                "fault_type",
                "sensor_group",
                "n_pairs",
                "median_difference",
                "p_value",
                "holm_p_value",
                "significant",
            ]
        ].to_string(index=False)
    )


if __name__ == "__main__":
    main()
