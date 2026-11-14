# Detect Dropped and Duplicated Sensor Frames

Report missing frame identifiers and repeated identifiers in an ordered sensor log.

```python
def audit_frame_ids(frame_ids):
```

## Contract

Frame IDs must be a nondecreasing vector of integers in [0,100000]. Integer-valued floating inputs are accepted. Return a dict with `missing`: every absent ID between the first and last observed IDs, ascending; and `duplicates`: each ID occurring more than once, once, ascending. Empty input returns two empty int64 arrays. No losses before/after the observed range are inferred.

**Shapes and outputs:** Nondecreasing integer-valued (N,) -> dict with int64 missing(K,) and duplicates(J,).

**Units:** frame_ids: integer sequence counter. **Time:** Log order is capture order; counters do not wrap or reset within one call.

Numeric inputs are converted with np.asarray and must then have integer or floating dtype (CPU). Boolean, string, complex, and object dtypes are rejected; mixed lists follow NumPy coercion. NaN/Inf and magnitudes above 1e9 raise ValueError. Other contract violations also raise ValueError. Do not mutate inputs. Outputs are new arrays unless stated otherwise. Numerical tolerance: rtol=1e-7, atol=1e-9. Runtime: Python 3.12.3, NumPy 2.2.4; 18 s wall, 10 s CPU, 4096 MiB address space, 64 KiB output. Fixtures are original synthetic CC0-1.0 data.

## Worked examples

1. `[3,4,4,6]` → `{"missing": [5], "duplicates": [4]}`.
2. `[7,7,7]` → `{"missing": [], "duplicates": [7]}`; the repeated ID is listed once.
