# Compute Transmittance and Alpha Compositing Weights

Turn ordered ray densities and metric interval lengths into sample visibility weights and remaining background mass.

```python
def alpha_compositing_weights(density: np.ndarray, deltas: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
```

## Contract

Compute a visibility weight for every sampled ray interval and return the probability mass that remains after the final interval. `density` and `deltas` are NumPy `float64` arrays of identical shape `(R,S)`, with positive dimensions and at most `1_000_000` elements each. Every entry is finite and lies in `[0,1e6]`.

Intervals are already in near-to-far order. Density is constant within each interval and has inverse-metre units; `deltas` contains physical interval lengths in metres. Ray directions were normalized upstream. The last interval is explicitly supplied just like the others; do not append an infinite interval. Zero density and zero-length intervals are valid.

For optical thickness `q = density * deltas`, use `alpha_i = 1-exp(-q_i)`, exclusive transmittance `T_i = exp(-sum(q_j for j<i))`, weight `w_i=T_i*alpha_i`, and background `exp(-sum(q_i))`. Return `(weights, background)` with shapes `(R,S)` and `(R,)`, both `float64`. Arrays are new, finite, nonnegative, and independent of inputs; inputs remain unchanged. Support noncontiguous arrays. Underflow to zero for an opaque interval or background is valid. Numerically stable `expm1` is useful for tiny positive thickness.

The weights need not sum to one by themselves; weights plus background must do so within `rtol=1e-6, atol=1e-7`. Do not renormalize weights, clamp a positive transmittance to an epsilon, or sort intervals. This task computes neither colors nor depth.

Raise `TypeError` when an argument is not a NumPy array. Raise `ValueError` for every other violation, including wrong dtype, shape, empty dimension, negative values, NaN/Inf, or bound violation. Invalid tests contain one violation. There are no timestamps; the caller is responsible for a consistent static scene snapshot.

## Example 1: two half-opaque intervals

```python
density = np.array([[np.log(2), np.log(2), 0.0]], dtype=np.float64)
deltas = np.array([[1.0, 1.0, 2.0]], dtype=np.float64)
alpha_compositing_weights(density, deltas)
# (array([[0.5, 0.25, 0.0]]), array([0.25]))
```

The first interval consumes half the incoming mass. The second consumes half of the remaining half. The zero-density last interval consumes nothing, leaving a quarter for the background.

## Example 2: length affects opacity

```python
density = np.array([[0.0, np.log(4), np.log(2)]], dtype=np.float64)
deltas = np.array([[3.0, 0.5, 1.0]], dtype=np.float64)
alpha_compositing_weights(density, deltas)
# (array([[0.0, 0.5, 0.25]]), array([0.25]))
```

The middle optical thickness is `log(4)*0.5 = log(2)`, so its opacity is one half. Density alone is not opacity. For any all-zero `deltas`, the corresponding result is all-zero weights and background one.

## Runtime

Python 3.12.3 on the local CPU sandbox. The shared worker enforces 18 seconds wall time, 10 seconds CPU, 4 GiB address space, and 64 KiB output. Dependency versions are pinned in this problem’s metadata. No GPU, downloaded model, or external dataset is required.

## Hints

## Hint 1

Compute optical thickness first. Its units cancel, which helps catch a missing or double-applied interval length.

## Hint 2

Build an exclusive accumulation: the first prefix is zero, and interval i uses only values before i.

## Hint 3

Use a stable opacity formula, keep the leftover background, and verify the two half-opaque intervals before trying a long ray.
