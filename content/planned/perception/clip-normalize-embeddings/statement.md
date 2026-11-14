# Normalize Image and Text Embeddings

**Status: drafted; not runnable yet.**

Normalize paired image and text feature rows while preserving the PyTorch gradient path.

```python
def normalize_clip_embeddings(image_features: torch.Tensor,
                              text_features: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
```

## Contract

Return `(unit_images, unit_texts)` by independently dividing each feature row by its Euclidean norm. Do not form logits, apply temperature, or compute the contrastive loss.

Inputs are CPU PyTorch tensors of the same dtype (`float32` or `float64`) and the same shape `(B,D)`, with `1 <= B <= 1024`, `1 <= D <= 4096`, and at most `1_000_000` elements each. All values are finite. Each row's mathematical L2 norm must lie in `[1e-6,1e6]`; boundary validation uses the norm after conversion to float64. This declared numerical range keeps the exercise focused on row semantics and gradients rather than extreme-value arithmetic. It is a teaching bound, not a property guaranteed by CLIP.

Both outputs keep shape, dtype, device, and row order. Norms are one within `rtol=1e-6, atol=1e-7`. Each output must be a new tensor with independent storage; do not modify either input. Support noncontiguous inputs. If an input requires gradients, its normalization must retain a differentiable connection to that input. Do not detach, convert through NumPy, or wrap the operation in `no_grad`. Inputs with no gradient requirement produce ordinary tensors.

Raise `TypeError` for a non-tensor argument. Raise `ValueError` for all remaining violations: mismatched or empty shape, unsupported/mixed dtype, non-CPU device, NaN/Inf, or out-of-range row norm. Zero vectors are rejected rather than given an arbitrary direction. Invalid tests contain one violation.

Embedding values are dimensionless and are not 3D points. Rows preserve existing image/caption pairing; this function receives no camera pose or timestamp.

## Example 1: independent row norms

```python
images = torch.tensor([[3., 4.], [0., -2.]], dtype=torch.float64)
texts  = torch.tensor([[0., 5.], [-8., 6.]], dtype=torch.float64)
normalize_clip_embeddings(images, texts)
# (tensor([[0.6, 0.8], [0.0, -1.0]], dtype=torch.float64),
#  tensor([[0.0, 1.0], [-0.8, 0.6]], dtype=torch.float64))
```

Image row norms are 5 and 2; text row norms are 5 and 10. Negative feature components remain negative.

## Example 2: equal directions, different magnitudes

```python
images = torch.tensor([[2., 0., 0.], [20., 0., 0.]], dtype=torch.float32)
texts  = torch.tensor([[0., 0., -7.], [0., 0., -0.5]], dtype=torch.float32)
normalize_clip_embeddings(images, texts)
# (tensor([[1., 0., 0.], [1., 0., 0.]]),
#  tensor([[0., 0., -1.], [0., 0., -1.]]))
```

Positive rescaling changes length but not normalized direction. Neither example changes the image-to-caption row pairing.

## Planned evaluation budget

Python 3.12.3, CPU, torch 2.6.0. Proposed limit: 3 seconds wall time, 2 seconds CPU time, 512 MiB memory, 64 KiB output. Image packaging and budget calibration are pending; this draft is not executable in the application.
