# Validate a Multimodal Robot Episode Schema

A robot-data pipeline combines images, joint positions and actions. An array may have the expected shape while using the wrong unit or coordinate frame. Implement a validator that returns every supported anomaly as a located, deterministic issue.

~~~python
validate_episodes(episodes, schema) -> list[dict]
~~~

## Schema

schema is a dictionary with signals, a dictionary keyed by nonempty signal names. Each signal specification contains:

| Field | Contract |
|---|---|
| shape | List of positive integer dimensions per timestamp; [] means one scalar |
| dtype | "float", "int", or "bool" |
| required | Boolean, default True |
| unit, frame | Optional exact string metadata |
| min, max | Optional finite inclusive bounds, min ≤ max |
| max_missing_fraction | Number in [0,1], default 0 |

schema.allow_extra_signals is a boolean, default True. Bad schema settings or a non-list episodes argument raise ValueError.

## Episodes and values

Every episode is a dictionary with timestamps (a list of finite numeric seconds, strictly increasing) and signals (a dictionary). Empty timestamps produce an issue. Each supplied signal is a dictionary with values (a list of length T) plus optional unit/frame strings. Each value row must match the per-time shape. None marks one missing row.

The float dtype accepts integer or floating numeric arrays. int accepts integer arrays only. bool accepts boolean arrays only. Object/string arrays fail dtype. Nonfinite numeric rows produce nonfinite instead of range issues; shape failures skip dtype/range checks for that row. Missing rows are counted in one signal-level missing_fraction issue when their fraction strictly exceeds the limit. No per-row issue is emitted for None.

A missing required signal produces missing; a missing optional signal is allowed. Extra signals are reported only when allow_extra_signals=False.

## Output and issue codes

Each issue has exactly:

~~~python
{"episode": 0, "path": "signals.joints.values[2]", "code": "range"}
~~~

Sort by (episode,path,code), lexicographically for string fields. Do not modify input data.

| Condition | Path | Code |
|---|---|---|
| Episode is not a dict | "" | type |
| timestamps is not a list | timestamps | type |
| timestamps is empty | timestamps | empty |
| Timestamp is nonnumeric, bool, NaN or Inf | timestamps[i] | nonfinite |
| Valid timestamp ≤ preceding valid adjacent timestamp | timestamps[i] | nonmonotonic |
| signals is not a dict | signals | type |
| Missing required / unexpected signal | signals.name | missing / unexpected |
| Signal is not a dict | signals.name | type |
| Declared unit/frame missing or mismatched | signals.name.unit or .frame | metadata |
| values is not a list / has wrong length | signals.name.values | type / length |
| Too many None rows | signals.name.values | missing_fraction |
| Row shape, dtype, finiteness or bounds violation | signals.name.values[i] | shape / dtype / nonfinite / range |

An invalid timestamps container stops further validation of that episode. A bad signals container stops signal checks. A bad values container or length stops row checks for that signal. Timestamp value errors do not prevent signal validation.

## Examples

**Example 1 — one valid joint signal**

~~~python
schema = {"signals": {"joints": {
    "shape": [2], "dtype": "float", "unit": "rad",
    "frame": "robot", "min": -3., "max": 3.
}}}
episodes = [{
    "timestamps": [0., 0.1],
    "signals": {"joints": {
        "values": [[0., 1.], [1., 2.]],
        "unit": "rad", "frame": "robot"
    }}
}]
# []
~~~

**Example 2 — stale time and out-of-range command**

Change the timestamps to [0.,0.] and the second joint row to [4.,2.]. Return:

~~~python
[
  {"episode": 0, "path": "signals.joints.values[1]", "code": "range"},
  {"episode": 0, "path": "timestamps[1]", "code": "nonmonotonic"}
]
~~~

The signal issue sorts before the timestamp issue.

## Boundaries

This task validates a declared contract. It does not transform frames, convert units, infer schemas, decode image bytes, detect semantic label errors, or certify robot safety. RGB fixtures use tiny arrays, not actual private camera recordings.

Sources: [Data Validation for ML](https://research.google/pubs/data-validation-for-machine-learning/), [Open X-Embodiment](https://arxiv.org/abs/2310.08864).
