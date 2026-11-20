# One Window, 100 Samples

This example shows how one 10-second window at **10 Hz** becomes a window feature row.

## Files

| File | One row is | Rows |
|---|---|---:|
| `sample_window_current_raw.csv` | one raw current sample | 100 |
| `sample_window_current_features.csv` | one window feature vector | 1 |

## Raw data

`sample_window_current_raw.csv` contains:

- `sample_index`: 0–99
- `time_s`: 0.0–9.9 seconds
- `current_a`: current in amperes

At 10 Hz:

```text
10 samples/second × 10 seconds = 100 samples
```

## Window features

The single feature row contains:

| Feature | Meaning |
|---|---|
| `n_samples` | number of raw samples in the window |
| `duration_s` | window duration |
| `sampling_hz` | sampling rate |
| `current_mean` | mean current |
| `current_std` | sample standard deviation |
| `current_min` | minimum current |
| `current_max` | maximum current |
| `current_median` | median current |
| `current_rms` | root mean square |
| `current_slope_a_per_s` | linear trend in A/s |
| `current_range` | max − min |
| `current_first` | first sample |
| `current_last` | last sample |

## How this becomes a window row

A model-ready window row would look like:

```text
unit_id, visit_id, trial_id, window_index,
current_mean, current_std, current_min, current_max,
current_slope_a_per_s, current_rms, ...
```

This example only covers the `current` channel. A full window row also contains the other channels measured during the same 10 seconds:

- voltage
- power
- ambient temperature/humidity
- inlet/outlet/coil temperatures
- vibration features
- airflow

## Important

The current mock data in `mock_data/minimum/` and `mock_data/ideal/` is simplified: it stores one window-level value per feature, not the raw 100-sample series. This example makes the raw-to-feature step explicit.

The scoring step after this is:

```text
100 raw samples
    → window features
    → z-score against healthy baseline
    → mean absolute z within a sensor group
    → one window score
```

Then six window scores are aggregated to one trial score by median.
