# Estimate Clock Offset from Paired Events

Estimate a constant clock offset from corresponding event timestamps using a robust median.

```python
def estimate_clock_offset(clock_a, clock_b):
```

## Contract

Accept paired timestamps in any row order; length must agree and be positive. Offset is median(clock_b-clock_a), averaging the middle two differences for even N. Return residuals clock_b-clock_a-offset in original row order. Do not sort residuals. Timestamps need not be increasing because pairing is already supplied.

**Shapes and outputs:** Two same-length nonempty (N,) -> (float offset, float64 residuals(N,)).

**Units:** timestamps: seconds, offset: seconds, residuals: seconds. **Time:** Rows are paired events; clock_b approximately equals clock_a plus offset. No rate drift is fitted.

Numeric inputs are converted with np.asarray and must then have integer or floating dtype (CPU). Boolean, string, complex, and object dtypes are rejected; mixed lists follow NumPy coercion. NaN/Inf and magnitudes above 1e9 raise ValueError. Other contract violations also raise ValueError. Do not mutate inputs. Outputs are new arrays unless stated otherwise. Numerical tolerance: rtol=1e-7, atol=1e-9. Runtime: Python 3.12.3, NumPy 2.2.4; 18 s wall, 10 s CPU, 4096 MiB address space, 64 KiB output. Fixtures are original synthetic CC0-1.0 data.

## Worked examples

1. `clock_a=[0,1,2], clock_b=[2,3,11]` → `(2.0,[0,0,7])`. One delayed event does not move the median.
2. `clock_a=[1,2], clock_b=[0,3]` → `(0.0,[-1,1])`. The two middle differences average to zero.
