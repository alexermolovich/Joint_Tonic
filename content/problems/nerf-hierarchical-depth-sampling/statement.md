# Sample Hierarchical Depth Intervals

Coarse rendering weights tell a fine sampler where useful mass lies along a ray. Inverse-CDF sampling converts supplied quantiles into depths. The small mass floor keeps every interval reachable without needing a random generator inside the task.

```python
def hierarchical_samples(edges, weights, quantiles):
    ...
```

## Function contract

Inputs: `edges: float64(B, S+1)`, `weights: float64(B, S)` and `quantiles: float64(B, K)`. Bounds: `1<=B<=32`, `1<=S, K<=128`. Depth edges are meters in `[0, 1000]`, strictly increasing with every gap at least `1e-9`. Weights are nonnegative and at most `1e6`; quantiles lie in `[0, 1]` and may be in arbitrary order.

Add `1e-5` to every weight, normalize masses per ray, and construct `CDF = [0, cumsum(probabilities)]`, setting the final entry exactly to 1. For each quantile use right-sided search, subtract one, and clip the interval index to `[0, S-1]`. Linearly interpolate from that CDF interval into its metric edge interval.

Return `float64(B, K)` depths preserving quantile order. Quantiles 0 and 1 return the near/far edges. Do not multiply masses by interval widths; supplied weights are masses, not densities. There is no random draw or field-network evaluation.

## Validation and execution

All arrays must be NumPy arrays with the exact stated `float64`, `int64` or `bool` dtype. Validate every entry, including masked entries: numeric inputs must be finite with absolute value at most 1e6, and each input array may contain at most 2,000,000 entries. More specific bounds below take precedence. Built-in Python `int`/`float` scalars exclude `bool`; sizes require built-in `int`. All type, shape and range violations raise `ValueError`. Noncontiguous CPU arrays are supported. Preserve every input and return fresh arrays with no shared storage between inputs or outputs. No implicit batching is accepted.

Runtime: Python 3.12.3 and NumPy 2.2.4; 18 seconds wall time, 10 seconds CPU, 4096 MiB address space and 64 KiB output. Numerical comparisons use `rtol=1e-6, atol=1e-7`. Fixtures are original synthetic CC0-1.0 data; no model checkpoint or external dataset is downloaded.

## Worked examples

**Example 1.** Edges `[[0, 1, 3]]`, weights `[[0, 0]]` and quantiles `[[0,.25,.5,.75, 1]]` produce depths `[[0,.5, 1, 2, 3]]`.

**Example 2.** A single interval with edges `[[2, 6]]`, weight `[[5]]` and quantiles `[[.75,.25]]` produces `[[5, 3]]`, preserving the unsorted query order.

## Source and scope

Original bounded component based on [2020-nerf](https://arxiv.org/abs/2003.08934). A neural scene model can spend more field queries near visible surfaces. Multiplying supplied masses by interval widths again biases the sampling distribution. This component does not evaluate a field, train NeRF or certify obstacle occupancy.
