# Add Noise to an Action Sequence

A diffusion policy learns to recover structured action chunks from noisy versions. Implement the deterministic forward process used to build one training example. The evaluator supplies noise explicitly so the same inputs always produce the same target.

~~~python
diffuse_actions(actions, alpha_bar, timesteps, noise, mask=None)
# -> (noised, target_noise)
~~~

## Inputs

- actions and noise: finite floating tensors with the same positive shape **(B,H,D)**, dtype and device.
- alpha_bar: finite 1-D tensor of length S ≥ 1, same dtype/device, nonincreasing values in [0,1].
- timesteps: int64 tensor of shape (B,), same device, indices in [0,S−1].
- mask: None or boolean tensor of shape (B,H), same device. True is a real action step; False is padding.

Each action dimension retains the units of the normalized training representation. In practice normalization is frozen before diffusion. H is a horizon index, not a physical time in seconds; the caller stores the control period separately.

Gather alpha_bar[timesteps[b]] for each batch member, broadcast it over H and D, and combine clean actions with noise using square-root weights. Return noise as the target. Set both returned tensors to zero wherever mask is False.

Outputs keep the input shape, dtype and device. Preserve gradients with respect to actions and noise and do not modify inputs or use any random generator.

## Examples

**Example 1 — pure signal and pure noise**

~~~python
actions = torch.tensor([[[2.]], [[4.]]])
noise = torch.tensor([[[10.]], [[20.]]])
alpha_bar = torch.tensor([1., 0.])
timesteps = torch.tensor([0, 1], dtype=torch.int64)
# noised = [[[2.]], [[20.]]]
# target_noise = [[[10.]], [[20.]]]
~~~

The two batch items gather different schedule values.

**Example 2 — equal signal and noise weights**

For actions=[[[2.]]], noise=[[[4.]]], alpha_bar=[0.5] and timestep=[0], noised is approximately [[[4.2426407]]], since both coefficients are sqrt(0.5).

**Example 3 — padding**

For mask=[[True,False]], the second horizon step is zero in both outputs, regardless of its clean action or noise value. Validate finite inputs even where padding will later be masked.

## Errors and limits

Raise TypeError when any of the four required inputs is not a tensor. Raise ValueError for all tensor-contract violations, including malformed masks, integer actions, increasing schedules, invalid indices, and NaN/Inf. The graded runtime uses float32/float64 CPU tensors. Time and memory are O(BHD).

## Hints

- The gathered coefficient needs shape (B,1,1).
- The mask needs an additional final axis to broadcast across action channels.
- The forward process is a direct formula; no iterative denoising is involved.

Source: [Diffusion Policy](https://arxiv.org/abs/2303.04137). This exercise covers training-data construction, not a trained policy or reverse sampler.
