# Encode Symlog Two-Hot Reward Targets

A signed logarithm compresses large reward magnitudes without losing their sign. Two neighboring bins preserve the transformed value by interpolation instead of abruptly rounding it to one class.

## Contract

```python
def symlog_twohot(rewards, bins):
    ...
```

rewards real (N,), 0<=N<=4096, abs<=1e6; bins real (K,), 2<=K<=255, strictly increasing within[-20,20]. Compute y=sign(reward)*log1p(abs(reward)); clip y into [bins0,binsLast]. Encode as two adjacent weights (b_hi-y)/(b_hi-b_lo) and (y-b_lo)/(b_hi-b_lo). Exact bin centers are one-hot; values outside support use endpoint one-hot. Return dict symlog float64(N,) BEFORE clipping, targets float64(N,K), reconstructed float64(N,) sign(mean)*expm1(abs(mean)) where mean=targets@bins. Enforce N*K<=1e6. This decoded value reconstructs clipped targets; no logits or predicted distribution are consumed. Bins have transformed dimensionless reward units and are supplied explicitly; not a hardcoded claim about every Dreamer revision.

Unless a tighter bound is stated below, numeric array-like inputs must have real integer/floating dtype after `np.asarray`, be finite with absolute values <=1e6 and at most 1,000,000 entries. Boolean, complex, string and object numeric arrays are invalid; Boolean masks must have Boolean dtype. Integer arrays/scalars exclude booleans. All invalid inputs raise ValueError. Return new arrays, preserve inputs, and compute floating outputs in float64 on CPU. No automatic differentiation is required.

## Physical context and scope

Latents and normalized actions are dimensionless. Rewards/values use a fixed caller-declared dimensionless reward scale; KL is measured in nats. Each ordered index is one fixed caller-declared control interval. Predicted continuation is a probability, not an elapsed duration. No implicit frame conversion. A bounded component with supplied tensors. Prediction loss inputs and deterministic imagined dynamics do not reproduce the complete trained recurrent stochastic world model, actor or benchmark.

## Example 1

Rewards[0,exp(1)-1], bins[-1,0,2] -> symlog[0,1], targets[[0,1,0],[0,.5,.5]], reconstructed equals supplied rewards.

## Example 2

Rewards[-100,100],bins[-1,0,1] -> endpoint one-hot rows[1,0,0],[0,0,1], reconstructed[-(exp(1)-1),exp(1)-1].
