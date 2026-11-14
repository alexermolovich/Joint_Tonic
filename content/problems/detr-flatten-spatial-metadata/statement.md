# Flatten Spatial Features with Position and Padding Metadata

Flattening is bookkeeping with physical consequences: a feature vector, its position and its padding flag must continue to refer to the same image location. Keep content and positional tokens separate so the downstream attention layer decides how to combine them.

```python
def flatten_spatial(features, positions, valid):
    ...
```

## Function contract

Inputs: `features: float64(B, H, W, D)`, `positions: float64(H, W, D)` and `valid: bool(B, H, W)`. Bounds: `1<=B<=16`, `1<=H, W<=32`, `1<=D<=32`.

Flatten spatial locations in row-major order: `index = row*W + column`. Return `tokens: float64(B, H*W, D)`, `position_tokens: float64(B, H*W, D)`, `padding: bool(B, H*W)` and `coordinates: int64(H*W, 2)`. Content and positional vectors stay separate; do not add them. Both vectors must be zero at invalid locations. Padding is the logical inverse of validity. Coordinates store `(row, column)` for every original grid location, including invalid ones.

Feature channels are dimensionless. Image indices point down/right for row/column. No image resize, camera transform or timestamp operation occurs.

## Validation and execution

All arrays must be NumPy arrays with the exact stated `float64`, `int64` or `bool` dtype. Validate every entry, including masked entries: numeric inputs must be finite with absolute value at most 1e6, and each input array may contain at most 2,000,000 entries. More specific bounds below take precedence. Built-in Python `int`/`float` scalars exclude `bool`; sizes require built-in `int`. All type, shape and range violations raise `ValueError`. Noncontiguous CPU arrays are supported. Preserve every input and return fresh arrays with no shared storage between inputs or outputs. No implicit batching is accepted.

Runtime: Python 3.12.3 and NumPy 2.2.4; 18 seconds wall time, 10 seconds CPU, 4096 MiB address space and 64 KiB output. Numerical comparisons use `rtol=1e-6, atol=1e-7`. Fixtures are original synthetic CC0-1.0 data; no model checkpoint or external dataset is downloaded.

## Worked examples

**Example 1.** For a one-row grid, features are `[2, 4]`, positions `[10, 20]` and validity `[True, False]`, each with one channel. Output tokens `[2, 0]`, positional tokens `[10, 0]`, padding `[False, True]`, coordinates `[[0, 0],[0, 1]]` (batch/channel dimensions retained).

**Example 2.** Mark both pixels invalid. Output content and positional arrays are zero, padding is `[True, True]`, and coordinates remain `[[0, 0],[0, 1]]`.

## Source and scope

Original bounded component based on [2020-detr](https://arxiv.org/abs/2005.12872). A detector can attend to the wrong location if position vectors use column-major order while features use row-major order. Padded regions must stay masked even when their zero features resemble a real dark region.
