# Encode Synchronized Observations for an Action Denoiser

A policy needs an observation context with a fixed temporal layout. This original small encoder makes that contract visible: pool an image, project it alongside proprioception, and preserve time order. A missing sensor is not equivalent to a valid zero measurement.

```python
def encode_observation_window(images, proprio, image_valid, proprio_valid, vision_weight, proprio_weight, bias):
    ...
```

## Function contract

Inputs are `images: float64(B, T, C, H, W)` with intensities in `[0, 1]`, normalized dimensionless `proprio: float64(B, T, P)`, `image_valid` and `proprio_valid` as `bool(B, T)`, `vision_weight: float64(C, D)`, `proprio_weight: float64(P, D)` and `bias: float64(D,)`. Bounds: `1<=B, T<=8`, `1<=C<=3`, `1<=H, W<=32`, `1<=P, D<=32`.

All time indices are already synchronized and chronological, with one episode per batch row; do not interpolate. Mean-pool images over H and W, then compute `pooled_image @ vision_weight + proprio @ proprio_weight + bias`. A slot is used only when both modality masks are true; unused contexts are zero.

Return `tokens: float64(B, T, D)`, `flat: float64(B, T*D)` and `used: bool(B, T)`. Flatten in chronological row-major order and give tokens/flat separate storage. This original linear encoder is a teaching substitute for a trained CNN, not Diffusion Policy's visual backbone.

## Validation and execution

All arrays must be NumPy arrays with the exact stated `float64`, `int64` or `bool` dtype. Validate every entry, including masked entries: numeric inputs must be finite with absolute value at most 1e6, and each input array may contain at most 2,000,000 entries. More specific bounds below take precedence. Built-in Python `int`/`float` scalars exclude `bool`; sizes require built-in `int`. All type, shape and range violations raise `ValueError`. Noncontiguous CPU arrays are supported. Preserve every input and return fresh arrays with no shared storage between inputs or outputs. No implicit batching is accepted.

Runtime: Python 3.12.3 and NumPy 2.2.4; 18 seconds wall time, 10 seconds CPU, 4096 MiB address space and 64 KiB output. Numerical comparisons use `rtol=1e-6, atol=1e-7`. Fixtures are original synthetic CC0-1.0 data; no model checkpoint or external dataset is downloaded.

## Worked examples

**Example 1.** With every dimension equal to 1, image `.5`, proprioception `2`, vision weight `3`, proprioception weight `4`, bias `1` and both masks true, return tokens `[[[10.5]]]`, flat `[[10.5]]` and used `[[True]]`.

**Example 2.** Keep the same data but mark proprioception invalid. Return tokens `[[[0]]]`, flat `[[0]]` and used `[[False]]`. A valid zero pixel would not itself invalidate the slot.

## Source and scope

Original bounded component based on [2023-diffusion-policy](https://arxiv.org/abs/2303.04137). A robot policy can react incorrectly when image and joint-state features are out of sync or reordered. This task assumes alignment is already done; zeroing unavailable observations prevents fabricated context but is not a replacement for a fallback controller.
