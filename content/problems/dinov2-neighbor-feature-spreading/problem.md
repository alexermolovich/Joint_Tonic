# Implement Nearest-Neighbor Feature-Spreading Regularization

A representation can collapse when many images receive nearly identical features. A nearest-neighbor spreading penalty discourages crowding on the unit sphere. It is possible for this loss to be negative: distances greater than one have positive logarithms.

```python
def neighbor_spreading(features, epsilon):
    ...
```

## Function contract

Input `features` is `float64(N, D)`, with `2<=N<=128`, `1<=D<=64` and each row's L2 norm at least `1e-9`. Python real `epsilon` lies in `[1e-8, 0.1]`.

Normalize each row to unit L2 norm. For each row, find its closest OTHER row in Euclidean distance, choosing the smallest original row index on ties. Return `distances: float64(N,)`, `neighbors: int64(N,)` and `loss: Python float`, equal to `-mean(log(max(distance, epsilon)))`.

Distances are returned unclamped; epsilon affects only the logarithm. Duplicate features are allowed and have distance zero. This is an explicitly clamped KoLeo-style teaching convention, not a claim to match every numerical detail of the released implementation. No gradients or encoder training are requested.

## Validation and execution

All arrays must be NumPy arrays with the exact stated `float64`, `int64` or `bool` dtype. Validate every entry, including masked entries: numeric inputs must be finite with absolute value at most 1e6, and each input array may contain at most 2,000,000 entries. More specific bounds below take precedence. Built-in Python `int`/`float` scalars exclude `bool`; sizes require built-in `int`. All type, shape and range violations raise `ValueError`. Noncontiguous CPU arrays are supported. Preserve every input and return fresh arrays with no shared storage between inputs or outputs. No implicit batching is accepted.

Runtime: Python 3.12.3 and NumPy 2.2.4; 18 seconds wall time, 10 seconds CPU, 4096 MiB address space and 64 KiB output. Numerical comparisons use `rtol=1e-6, atol=1e-7`. Fixtures are original synthetic CC0-1.0 data; no model checkpoint or external dataset is downloaded.

## Worked examples

**Example 1.** Features `[[1, 0],[-1, 0]]` with epsilon `.01` return distances `[2, 2]`, neighbors `[1, 0]`, and loss `-log(2)`.

**Example 2.** Three identical nonzero feature rows return distances `[0, 0, 0]`, neighbors `[1, 0, 0]`, and loss `-log(epsilon)`. The diagonal is excluded even when other rows are duplicates.

## Source and scope

Original bounded component based on [2023-dinov2](https://arxiv.org/abs/2304.07193). Reusable visual features should distinguish different scenes before a robot policy consumes them. Accidentally selecting each feature as its own neighbor makes every distance zero and destroys the intended learning signal.
