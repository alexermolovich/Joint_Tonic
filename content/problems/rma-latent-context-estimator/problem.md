# Estimate a Latent Dynamics Context

A temporal adaptation module turns normalized sensor/action history into policy context. Mask padding before temporal mixing and suppress empty histories instead of treating a learned bias as fresh evidence.

## Contract

`history` is real `(B, H, F)`, `valid` is Boolean `(B, H)`, `temporal_kernel` is real `(3, F, C)`, `weight` is real `(H*C, L)` and `bias` is real `(L,)`. Bounds are `1 <= B, H, F <= 32`, `1 <= C, L <= 16`; numeric magnitudes are at most 100. History is chronological normalized state/action data. Each mask row must be a suffix of true entries following optional false left padding; all-false is allowed.

Zero invalid history rows and pad one zero row at each temporal end. Compute width-three temporal cross-correlation without reversing the kernel: `conv[b,t,c] = sum(padded_history[b,t+k,f] * kernel[k,f,c])` over k and f. Apply ReLU, then zero every invalid temporal output. Flatten in chronological/channel order and apply the supplied linear weight and bias.

Return `latent` (float64 `(B, L)`) and `used` (Boolean `(B,)`, any valid history) in a dictionary. For an all-false history, return an exact zero latent rather than the bias. This original one-block adaptation surrogate is not the paper's full trained temporal network. It uses no privileged factors during inference.

Unless a tighter bound is stated below, numeric array-like inputs must have real integer/floating dtype after `np.asarray`, be finite with absolute values <=1e6 and at most 1,000,000 entries. Boolean, complex, string and object numeric arrays are invalid; Boolean masks must have Boolean dtype. Integer arrays/scalars exclude booleans. All invalid inputs raise ValueError. Return new arrays, preserve inputs, and compute floating outputs in float64 on CPU. No automatic differentiation is required.

## Physical context and scope

Normalized observations, extrinsics, actions and latents are dimensionless. Timestamps and ages use seconds. Synchronized fixed-period state/action history; episode and completion boundaries explicit. No implicit frame or clock conversion. Original bounded adaptation teaching component. Frozen encoder and temporal alternatives do not reproduce the complete trained RMA networks or hardware benchmark.

## Example 1

With B=H=F=C=L=1, history value 2, center kernel weight 3, head weight 4 and bias 1, the latent is 25 and used is true.

## Example 2

An all-false history returns latent 0 and used false even when the head bias is 1. A negative convolution value is clamped to zero before the head.
