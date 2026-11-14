# Worked examples

These original synthetic examples are public teaching material, not hidden evaluator fixtures. The [statement](#) is the complete contract.

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

## Theory question answers

1. A quarter of the incoming mass remains for the explicit background; the intervals are finite.
2. Numerical lengths increase100times, so density in inverse centimetres must be divided by100. Optical thickness stays unchanged.
