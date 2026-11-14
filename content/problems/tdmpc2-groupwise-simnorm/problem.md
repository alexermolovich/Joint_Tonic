# Apply Groupwise SimNorm to Latent States

SimNorm turns each small latent block into a probability simplex. Different blocks retain separate capacity; treating the entire vector as one softmax changes the representation.

## Contract

```python
def simnorm(latents, group_size):
    ...
```

latents real(B,D),0<=B<=4096,1<=D<=256, total<=1e6,abs<=1e6; group_size built-in int1..32 dividing D. Reshape final axis into consecutive groups of size group_size and apply stable softmax independently in each group. Return fresh float64(B,D). No global normalization or temperature parameter. Dimensionless latents, row-independent batches. The original SimNorm primitive; no learned encoder is included.

Unless a tighter bound is stated below, numeric array-like inputs must have real integer/floating dtype after `np.asarray`, be finite with absolute values <=1e6 and at most 1,000,000 entries. Boolean, complex, string and object numeric arrays are invalid; Boolean masks must have Boolean dtype. Integer arrays/scalars exclude booleans. All invalid inputs raise ValueError. Return new arrays, preserve inputs, and compute floating outputs in float64 on CPU. No automatic differentiation is required.

## Physical context and scope

Latents and normalized commands are dimensionless. Rewards and decoded critic values share the declared dimensionless score scale; inverse temperature has reciprocal score units. Each horizon index is one fixed caller-declared control interval. Termination occurs after the current transition reward. No implicit frame conversion or simulator execution. Bounded component informed by TD-MPC2 and the pinned official implementation. Affine dynamics and deterministic supplied critic/candidate inputs are declared teaching simplifications, not a trained world model or complete MPC controller.

## Example 1

latents[[0,0,1,1]],group 2 ->[[.5,.5,.5,.5]].

## Example 2

latents[[0,log(3),1000,1000]],group 2 ->[[.25,.75,.5,.5]].
