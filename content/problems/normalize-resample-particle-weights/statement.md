# Normalize and Resample Particle Weights

Normalize nonnegative particle weights and perform deterministic systematic resampling.

```python
def resample_particles(weights, offset):
```

## Contract

Weights must be nonnegative with positive total. Offset must be a scalar in [0,1). Divide by the maximum weight before summing to avoid underflow. Systematic positions are (offset+arange(N))/N. Return the first cumulative-weight index strictly greater than each position (searchsorted side="right"); force the last cumulative entry to 1 to absorb roundoff. Zero-weight particles must never be selected at an exact boundary. This function must not draw random numbers.

**Shapes and outputs:** weights(N,), 1<=N<=100000, scalar offset -> (float64 normalized(N,), int64 ancestry(N,)).

**Units:** weights: unnormalized likelihood mass, offset: dimensionless unit-interval fraction. **Time:** All particles describe the same state timestamp; no motion update is performed.

Numeric inputs are converted with np.asarray and must then have integer or floating dtype (CPU). Boolean, string, complex, and object dtypes are rejected; mixed lists follow NumPy coercion. NaN/Inf and magnitudes above 1e9 raise ValueError. Other contract violations also raise ValueError. Do not mutate inputs. Outputs are new arrays unless stated otherwise. Numerical tolerance: rtol=1e-7, atol=1e-9. Runtime: Python 3.12.3, NumPy 2.2.4; 18 s wall, 10 s CPU, 4096 MiB address space, 64 KiB output. Fixtures are original synthetic CC0-1.0 data.

## Worked examples

1. `weights=[1,0,2,1], offset=0.5` → normalized `[0.25,0,0.5,0.25]`, ancestry `[0,2,2,3]`.
2. `weights=[0,5], offset=0` → normalized `[0,1]`, ancestry `[1,1]`; a position of zero skips zero mass.

Numerical endpoint convention: clamp computed systematic positions to np.nextafter(1.0,0.0), because floating arithmetic can round a nominally subunit position to 1. This keeps ancestry indices in range.
