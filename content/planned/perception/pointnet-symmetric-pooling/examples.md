# Worked examples

These original synthetic examples are public teaching material, not hidden evaluator fixtures. The [statement](statement.md) is the complete contract.

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

## Theory question answers

1. Validity belongs to a particular point slot. Permuting features alone changes the valid set.
2. Duplicates do not change channel maxima. Removing a point that supplies a maximum can change them, so missing-point robustness does not follow.
