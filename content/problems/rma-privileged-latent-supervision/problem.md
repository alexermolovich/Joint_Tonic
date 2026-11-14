# Build Privileged Dynamics-Latent Supervision

Privileged simulator factors provide supervision that is unavailable on the deployed robot. Keep their teacher encoding fixed while measuring the adaptation prediction error.

## Contract

`extrinsics` is real `(B, E)`, `encoder_weight` is real `(E, L)`, `encoder_bias` is real `(L,)`, `predicted_latents` is real `(B, L)` and `valid` is Boolean `(B,)`. Bounds are `1 <= B <= 128`, `1 <= E, L <= 32`; numeric magnitudes are at most 100. Extrinsics are already normalized simulator-only factors; latent coordinates are dimensionless.

Define frozen teacher targets `z = tanh(extrinsics @ encoder_weight + encoder_bias)`. This one-layer encoder is a declared teaching surrogate for the learned environment encoder. Return a dictionary with `targets` (float64 `(B, L)`, z on valid rows and zero elsewhere), `per_state` (float64 `(B,)`, mean squared prediction error over L channels, NaN when invalid), `loss` (Python float, mean over valid state losses, or zero when none exist), and `prediction_gradient` (float64 `(B, L)`, twice the residual divided by valid-state count times L, zero on invalid rows).

Teacher targets and parameters remain fixed. Do not return teacher gradients, update an optimizer or claim this is the complete RMA encoder architecture.

Unless a tighter bound is stated below, numeric array-like inputs must have real integer/floating dtype after `np.asarray`, be finite with absolute values <=1e6 and at most 1,000,000 entries. Boolean, complex, string and object numeric arrays are invalid; Boolean masks must have Boolean dtype. Integer arrays/scalars exclude booleans. All invalid inputs raise ValueError. Return new arrays, preserve inputs, and compute floating outputs in float64 on CPU. No automatic differentiation is required.

## Physical context and scope

Normalized observations, extrinsics, actions and latents are dimensionless. Timestamps and ages use seconds. Synchronized fixed-period state/action history; episode and completion boundaries explicit. No implicit frame or clock conversion. Original bounded adaptation teaching component. Frozen encoder and temporal alternatives do not reproduce the complete trained RMA networks or hardware benchmark.

## Example 1

One factor 0, weight 1, bias 0, prediction 2 and a valid row yield teacher target 0, per-state and total loss 4, and prediction gradient 4.

## Example 2

Two target channels [0, 0] and prediction [1, -1] yield loss 1 and gradient [1, -1]. An entirely invalid batch has zero loss, targets and gradients, with NaN per-state losses.
