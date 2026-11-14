# Prove Permutation Invariance with Symmetric Pooling

Pool valid point features channel by channel and demonstrate that point order cannot change the result.

```python
def symmetric_point_pool(features: np.ndarray, valid_mask: np.ndarray | None = None) -> np.ndarray:
```

## Contract

Given per-point features, return the maximum valid value separately for each cloud and feature channel. The result is invariant to any point-axis permutation applied to both features and their mask. Explain that invariant in the accompanying theory question; the implementation grade checks it numerically.

`features` is a finite NumPy `float32` or `float64` array `(B,N,D)`, with all three dimensions positive and at most `1_000_000` elements. These are already computed features, not XYZ coordinates. `valid_mask` is either `None` (all slots valid) or a NumPy boolean array exactly `(B,N)`. Every cloud must have at least one valid slot. Require finite values even in masked slots so malformed data is reported consistently.

Return a newly allocated `(B,D)` array with the same dtype. Do not mutate or alias inputs. Support duplicate points, ties, negative features, and noncontiguous arrays. Padding must never influence the result; replacing masked values with zero is wrong when all valid values are negative. No learned weights, MLP, feature transform, gradient, or classifier is part of this task.

Raise `TypeError` when `features` is not an array or `valid_mask` is neither an array nor `None`. Raise `ValueError` for other violations, including wrong dtype/shape, any empty dimension, NaN/Inf, or an all-false mask row. Invalid tests contain one violation.

Feature axes are not spatial axes and have no physical length units. Source points must already share one frame and timestamp convention upstream; this function does not register clouds or compensate for motion.

## Example 1: a permutation changes nothing

```python
features = np.array([[[1., -2.], [3., -4.], [2., -1.]]], dtype=np.float64)
symmetric_point_pool(features)
# array([[3., -1.]])
symmetric_point_pool(features[:, [2, 0, 1], :])
# array([[3., -1.]])
```

The two channel maxima come from different points. Pooling is channel-wise, not selection of one whole point row.

## Example 2: exclude padding without introducing zero

```python
features = np.array([[[-5., -2.], [99., 99.], [-3., -8.]]], dtype=np.float32)
mask = np.array([[True, False, True]])
symmetric_point_pool(features, mask)
# array([[-3., -2.]], dtype=float32)
```

The padded `[99,99]` slot is ignored. Replacing it with `[0,0]` before taking maxima would incorrectly return `[0,0]`. Permuting the features without permuting `mask` is a different input, so invariance does not promise an equal result.

## Runtime

Python 3.12.3 on the local CPU sandbox. The shared worker enforces 18 seconds wall time, 10 seconds CPU, 4 GiB address space, and 64 KiB output. Dependency versions are pinned in this problem’s metadata. No GPU, downloaded model, or external dataset is required.

## Hints

## Hint 1

The point axis is axis 1, so the two remaining axes should be B and D.

## Hint 2

A mask of shape (B,N) needs a feature dimension when combined with (B,N,D). Invalid slots must be unable to win a maximum.

## Hint 3

To test invariance, use the same per-cloud permutation on feature rows and their validity mask. Also test all-negative valid features.
