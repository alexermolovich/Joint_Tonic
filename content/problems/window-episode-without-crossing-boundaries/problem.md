# Window an Episode Without Crossing Boundaries

Generate fixed-length row-index windows wholly contained in individual contiguous episodes.

```python
def episode_windows(episode_ids, window, stride):
```

## Contract

Episode IDs are nonnegative integer-valued numbers; an ID may not reappear after its run ends. window and stride must be positive Python or NumPy integers (not bool), each <=10000. Produce windows in row order; starts are run_start + k*stride, keeping only complete windows. An empty input is valid. No padding or window crossing is allowed.

**Shapes and outputs:** episode_ids(N,) -> int64(K,window), including (0,window).

**Units:** episode_ids: dimensionless IDs, window: frames, stride: frames. **Time:** Rows are chronological; each episode is a contiguous run. Stride restarts at each run.

Numeric inputs are converted with np.asarray and must then have integer or floating dtype (CPU). Boolean, string, complex, and object dtypes are rejected; mixed lists follow NumPy coercion. NaN/Inf and magnitudes above 1e9 raise ValueError. Other contract violations also raise ValueError. Do not mutate inputs. Outputs are new arrays unless stated otherwise. Numerical tolerance: rtol=1e-7, atol=1e-9. Runtime: Python 3.12.3, NumPy 2.2.4; 18 s wall, 10 s CPU, 4096 MiB address space, 64 KiB output. Fixtures are original synthetic CC0-1.0 data.

## Worked examples

1. `episode_ids=[4,4,4,8,8], window=2, stride=1` → `[[0,1],[1,2],[3,4]]`.
2. `episode_ids=[1,1,1,1,2], window=3, stride=2` → `[[0,1,2]]`; no partial window is returned.
