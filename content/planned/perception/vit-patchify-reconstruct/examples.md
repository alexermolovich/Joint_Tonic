# Worked examples

These original synthetic examples are public teaching material, not hidden evaluator fixtures. The [statement](statement.md) is the complete contract.

## Example 1: rectangular image

```python
image = np.array([[[[1, 2, 3, 4], [5, 6, 7, 8]]]], dtype=np.float32)
tokens = patchify(image, 2)
# array([[[1, 2, 5, 6], [3, 4, 7, 8]]], dtype=float32)
unpatchify(tokens, (1, 1, 2, 4), 2)
# array([[[[1, 2, 3, 4], [5, 6, 7, 8]]]], dtype=float32)
```

The left 2-by-2 patch precedes the right patch. A plain reshape into length-four vectors would incorrectly put `[1,2,3,4]` in the first token.

## Example 2: channel order inside one patch

```python
image = np.array([[[[1, 2], [3, 4]], [[10, 20], [30, 40]]]], dtype=np.float64)
tokens = patchify(image, 2)
# array([[[1, 2, 3, 4, 10, 20, 30, 40]]])
unpatchify(tokens, (1, 2, 2, 2), 2)
# array([[[[1, 2], [3, 4]], [[10, 20], [30, 40]]]])
```

All four samples from channel 0 precede channel 1. Interleaving channel values would be a different, invalid contract even if a matching inverse could undo it.

## Theory question answers

1. Both functions can share a wrong permutation and still cancel it. Check direct token values too.
2. Batch0, token1, element2: grid column1, channel0, local row1, local column0.
