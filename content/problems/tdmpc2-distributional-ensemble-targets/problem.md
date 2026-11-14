# Build Distributional Reward and Ensemble-Value Targets

A target critic ensemble can reduce optimistic bootstrapping, while transformed two-hot targets keep large returns from becoming arbitrary regression scales. Record which critics supplied the target so it can be reproduced.

## Contract

```python
def distributional_targets(rewards, next_values, critic_indices, terminated, bins, gamma):
    ...
```

rewards real(B,),next_values real(B,E),critic_indices int(B,2),terminated bool(B,),bins real(K,),gamma scalar[0,1];0<=B<=1024,2<=E<=16,2<=K<=255,all valuesabs<=1e6,bins increasing[-20,20]. Each row selects two DISTINCT ensemble columns in[0,E); take their minimum (not min of all critics). target_y=reward+gamma*(not terminated)*min_selected. Encode both reward and target_y using symlog sign(x)*log1p(abs(x)), clip to bins, and adjacent two-hot interpolation. Return dict bootstrap float64(B) selected minimum even if terminated, td_target float64(B), reward_targets/value_targets float64(B,K). Critic values are already decoded expected returns in reward units; no actor or random critic selection inside function. No gradients, targetnetwork updates or entropy subtraction. Original explicit supplied-index version of the paper/released clipped-ensemble target; the released implementation samples one pair shared over a batch, while this teaching contract accepts recorded per-row pairs; includes existing two-hot primitive as prerequisite.

Unless a tighter bound is stated below, numeric array-like inputs must have real integer/floating dtype after `np.asarray`, be finite with absolute values <=1e6 and at most 1,000,000 entries. Boolean, complex, string and object numeric arrays are invalid; Boolean masks must have Boolean dtype. Integer arrays/scalars exclude booleans. All invalid inputs raise ValueError. Return new arrays, preserve inputs, and compute floating outputs in float64 on CPU. No automatic differentiation is required.

## Physical context and scope

Latents and normalized commands are dimensionless. Rewards and decoded critic values share the declared dimensionless score scale; inverse temperature has reciprocal score units. Each horizon index is one fixed caller-declared control interval. Termination occurs after the current transition reward. No implicit frame conversion or simulator execution. Bounded component informed by TD-MPC2 and the pinned official implementation. Affine dynamics and deterministic supplied critic/candidate inputs are declared teaching simplifications, not a trained world model or complete MPC controller.

## Example 1

reward 1,next_values [2,10,4],indices [0,2],not terminated,gamma .5 ->bootstrap 2,td_target 2. With bins[0,log(2),log(3)],reward target [0,1,0],value target [0,0,1].

## Example 2

Same row terminated True ->td_target 1 and value target equals reward target, while reported bootstrap remains 2.
