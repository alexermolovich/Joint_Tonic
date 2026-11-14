# Compute a Conditional Noise-Prediction Loss

Draft for review; this is not a published or runnable problem.

## Task

A denoiser has predicted the noise added to a demonstrated action chunk. Compare its prediction with the supplied target noise and return mean squared error over valid action scalars only.

## Function

```python
def conditional_noise_loss(
    prediction: torch.Tensor,
    target_noise: torch.Tensor,
    valid: torch.Tensor,
) -> torch.Tensor:
    ...
```

- `prediction` and `target_noise` are CPU tensors with identical shape `(B,H,D)` and identical dtype, either float32 or float64. All values, including padding, must be finite and have magnitude at most `1e6`.
- `valid` is a CPU bool tensor `(B,H)`. At least one entry must be True. Bounds: `1<=B<=64`, `1<=H<=256`, `1<=D<=64`, at most `2_000_000` scalars per float input.
- Return a zero-dimensional tensor matching the float inputs’ dtype/device. Sum squared errors over valid entries and divide by `D*valid.sum()`. Every valid scalar has equal weight, even when examples contain different numbers of valid timesteps.
- Return a fresh scalar; do not mutate or alias inputs. Preserve autograd through both floating inputs. If targets should be detached in a training pipeline, that is the caller’s responsibility. Masked entries must have zero loss gradient.
- Noncontiguous tensors are supported. No randomness, model call, schedule lookup, sample weighting, per-item normalization, or conversion to a Python float is allowed.

The inputs are noise values in normalized action coordinates, not raw joint angles, clean actions, or physical timestamps. “Conditional” describes the upstream model, which already used the observation and diffusion level; this reduction does not take those inputs again.

## Errors and complexity

Raise `TypeError` if any argument is not a tensor. Raise `ValueError` for all tensor-contract violations: rank/shape, dtype/device, bounds, nonfinite/out-of-range values, non-bool validity, or an all-false mask. Validate masked entries too.

Time is `O(BHD)`, with at most `O(BHD)` temporary storage. Use numerically valid tensor operations; the magnitude/size bounds keep the specified float32 reduction within finite range.

## Worked examples

### Case1: padding does not contribute

```text
prediction = [[[1,3],[100,100]]]
target_noise = [[[0,1],[0,0]]]
valid = [[True,False]]

loss = scalar tensor2.5
```

The valid residual is[1,2], giving(1²+2²)/2=2.5. When prediction requires gradients, its gradient is[[[1,2],[0,0]]]. The padded100 values are finite but ignored by the objective.

### Case2: one global mean with unequal valid horizons

```text
prediction = [[[2],[0]], [[2],[4]]]
target_noise = [[[0],[0]], [[0],[0]]]
valid = [[True,False], [True,True]]

loss = scalar tensor8
```

There are three valid scalar errors:4,4,16. Their mean is8. Averaging per-item means would instead yield(4+10)/2=7, which is not this contract.

## Source and scope

This component computes the masked noise-regression reduction after a conditional denoiser has run. It does not build that network, sample timesteps/noise, construct noised actions, or duplicate the published forward-noising problem. Validity masking and the exact global reduction are explicit teaching contracts.

[Primary paper](https://arxiv.org/abs/2303.04137).
