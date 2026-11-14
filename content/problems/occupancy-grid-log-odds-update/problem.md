# Update Occupancy Grid Log Odds

Accumulate repeated occupancy observations in log-odds space with explicit clipping.

```python
def update_occupancy(log_odds, observations, prior, limit):
```

## Contract

Each observation row is [row,column,p], with integer-valued in-bounds indices and probability p strictly between 0 and 1. Prior is a scalar probability strictly between 0 and 1. Limit is a positive scalar; all initial log odds must lie in [-limit,limit]. For every observation, add log(p/(1-p))-log(prior/(1-prior)) to its cell, then clip immediately to [-limit,limit]. Unobserved cells are unchanged. Empty observations must have shape (0,3).

**Shapes and outputs:** log_odds(H,W), observations(N,3) -> fresh float64(H,W), H,W>=1.

**Units:** log_odds: dimensionless, observations: row, column, occupied probability, prior: occupied probability, limit: absolute log odds. **Time:** Observation rows are processed in arrival order; repeated cells accumulate evidence sequentially.

Numeric inputs are converted with np.asarray and must then have integer or floating dtype (CPU). Boolean, string, complex, and object dtypes are rejected; mixed lists follow NumPy coercion. NaN/Inf and magnitudes above 1e9 raise ValueError. Other contract violations also raise ValueError. Do not mutate inputs. Outputs are new arrays unless stated otherwise. Numerical tolerance: rtol=1e-7, atol=1e-9. Runtime: Python 3.12.3, NumPy 2.2.4; 18 s wall, 10 s CPU, 4096 MiB address space, 64 KiB output. Fixtures are original synthetic CC0-1.0 data.

## Worked examples

1. `log_odds=[[0]], observations=[[0,0,0.8],[0,0,0.8]], prior=0.5, limit=2` → `[[2.0]]`.
2. `log_odds=[[0.3,-0.2]], observations=[[0,1,0.7]], prior=0.7, limit=4` → `[[0.3,-0.2]]`; evidence equal to the prior is neutral.
