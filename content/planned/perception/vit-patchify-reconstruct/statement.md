# Patchify and Reconstruct an Image Tensor

**Status: drafted; not runnable yet.**

Convert channels-first images into ordered patch vectors and reconstruct every input pixel.

```python
def patchify(images: np.ndarray, patch_size: int) -> np.ndarray:
    ...

def unpatchify(patches: np.ndarray, image_shape: tuple[int, int, int, int],
               patch_size: int) -> np.ndarray:
```

## Contract

Write both functions. `patchify` converts `(B,C,H,W)` into `(B,N,C*P*P)`, where `P=patch_size` and `N=(H//P)*(W//P)`. `unpatchify` reverses that layout using the requested `image_shape=(B,C,H,W)`.

Arrays are NumPy `float32` or `float64`, with finite values. `0 <= B <= 1024` and `1 <= C,H,W <= 4096`. `P` must be a Python `int` in `[1,4096]`, excluding booleans, and divide both H and W. `image_shape` must be a length-four tuple of Python integers, excluding booleans, satisfying these same per-axis bounds. These limits also apply to zero-image batches. Each array contains at most `1_000_000` elements. Noncontiguous inputs are supported.

Patch traversal is **grid row, then grid column**. Inside each patch the flattened order is **channel, then local row, then local column**. Thus the fastest-moving index is the pixel column within a patch. This is a declared channels-first convention, not a claim that all ViT libraries use the same flattening order.

`unpatchify` requires its supplied array shape to exactly match `(B,(H//P)*(W//P),C*P*P)`. Do not infer a square image from token count. Both functions preserve dtype and values exactly, return independently owned arrays, and leave inputs unchanged. No normalization, channel permutation, interpolation, class token, or linear projection occurs. Pixels keep their existing intensity units and image frame; no timestamps are consumed.

Raise `TypeError` for a non-array first argument. Raise `ValueError` for all other violations, including malformed shape, invalid P, mismatched patch shape, unsupported dtype, or NaN/Inf. A zero-image batch returns the corresponding empty shape. Only one violation is supplied per invalid test.

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

## Planned evaluation budget

Python 3.12.3, CPU, numpy 2.2.4. Proposed limit: 3 seconds wall time, 2 seconds CPU time, 512 MiB memory, 64 KiB output. Image packaging and budget calibration are pending; this draft is not executable in the application.
