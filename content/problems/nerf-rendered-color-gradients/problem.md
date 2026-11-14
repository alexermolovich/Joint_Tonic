# Differentiate Rendered Color on a Small Synthetic Field

Increasing one sample's density makes its own color more visible and hides everything behind it. The gradient must account for both effects, including background. Differentiating only the local opacity misses the occlusion mechanism that trains a radiance field.

```python
def render_color_gradients(density, intervals, colors, background, target):
    ...
```

## Function contract

Inputs: `density: float64(B, S)`, `intervals: float64(B, S)`, `colors: float64(B, S, 3)`, `background: float64(3,)` and `target: float64(B, 3)`. Bounds: `1<=B<=32`, `1<=S<=128`. Density is in `[0, 1000]` inverse meters; intervals are in `[1e-9, 10]` meters along normalized rays. All RGB entries lie in `[0, 1]` and are linear RGB.

For ordered samples, compute opacity `alpha_i = 1-exp(-density_i*interval_i)`, exclusive transmittance `T_i = exp(-sum of earlier optical thicknesses)`, weight `w_i = T_i*alpha_i` and terminal transmittance over all intervals. Render the weighted RGB sum plus terminal transmittance times background. Loss is mean squared error over all B*3 RGB channels.

Return `rgb: float64(B, 3)`, `loss: Python float`, `density_gradient: float64(B, S)` and `color_gradient: float64(B, S, 3)`. Gradients are analytic derivatives of this scalar loss. Every density affects its own color, all downstream samples and background. No interval/background/target derivative, field MLP or autograd package is required. Full opacity may consistently underflow transmittance to zero.

## Validation and execution

All arrays must be NumPy arrays with the exact stated `float64`, `int64` or `bool` dtype. Validate every entry, including masked entries: numeric inputs must be finite with absolute value at most 1e6, and each input array may contain at most 2,000,000 entries. More specific bounds below take precedence. Built-in Python `int`/`float` scalars exclude `bool`; sizes require built-in `int`. All type, shape and range violations raise `ValueError`. Noncontiguous CPU arrays are supported. Preserve every input and return fresh arrays with no shared storage between inputs or outputs. No implicit batching is accepted.

Runtime: Python 3.12.3 and NumPy 2.2.4; 18 seconds wall time, 10 seconds CPU, 4096 MiB address space and 64 KiB output. Numerical comparisons use `rtol=1e-6, atol=1e-7`. Fixtures are original synthetic CC0-1.0 data; no model checkpoint or external dataset is downloaded.

## Worked examples

**Example 1.** One ray/sample has density `0`, interval `1`, red sample color `[1, 0, 0]`, and black target/background. Output RGB is `[0, 0, 0]`, loss `0`, and both gradient arrays are zero.

**Example 2.** Replace density by `log(2)`. Output RGB is `[.5, 0, 0]`, loss `1/12`, density gradient `1/6`, and color gradient `[1/6, 0, 0]`, with original batch/sample dimensions retained.

## Source and scope

Original bounded component based on [2020-nerf](https://arxiv.org/abs/2003.08934). Differentiable rendering connects image errors to a robot's learned scene representation. Ignoring background attenuation gives wrong gradients even for an empty-looking ray. A low RGB loss does not alone establish correct metric geometry or collision safety.
