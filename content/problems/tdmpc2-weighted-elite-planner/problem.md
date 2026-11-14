# Update a Sampling-Based Planner

A sampling planner concentrates its next proposal around high-scoring candidate sequences. Weighted population variance must be measured around the newly computed mean before enforcing exploration bounds.

## Contract

```python
def update_elite_distribution(actions, scores, valid, num_elites, inverse_temperature, min_std, max_std):
    ...
```

actions real(K,H,A) normalized[-1,1],scores real(K,)abs<=1e6,valid bool(K,);1<=K<=1024,1<=H<=64,1<=A<=32,total action entries<=1e6; num_elites built-in int1..K,require validcount>=num_elites; inverse_temperature scalar[0,100],min_std/max_std scalar0<=min<=max<=2. Select num_elites valid candidate indices by descending score then ascending original index. Compute normalized weights exp(inverse_temperature*(score-max_elite_score)). Return dict elite_indices int64(E,),weights float64(E,),mean float64(H,A)=weighted mean of eliteactions,std float64(H,A)=sqrt(weighted population variance around NEW mean),clamped[min_std,max_std]. Exact normalization (no extra denominator epsilon since at least one exponential=1). No oldmean momentum, randomsampling, actionselection or control execution. Supplied scores use a fixed dimensionless reward scale so inverse_temperature has reciprocal score units. Current official MPPI-style update motivates the component; deterministic ties and omitted tiny denominator epsilon are declared original conventions.

Unless a tighter bound is stated below, numeric array-like inputs must have real integer/floating dtype after `np.asarray`, be finite with absolute values <=1e6 and at most 1,000,000 entries. Boolean, complex, string and object numeric arrays are invalid; Boolean masks must have Boolean dtype. Integer arrays/scalars exclude booleans. All invalid inputs raise ValueError. Return new arrays, preserve inputs, and compute floating outputs in float64 on CPU. No automatic differentiation is required.

## Physical context and scope

Latents and normalized commands are dimensionless. Rewards and decoded critic values share the declared dimensionless score scale; inverse temperature has reciprocal score units. Each horizon index is one fixed caller-declared control interval. Termination occurs after the current transition reward. No implicit frame conversion or simulator execution. Bounded component informed by TD-MPC2 and the pinned official implementation. Affine dynamics and deterministic supplied critic/candidate inputs are declared teaching simplifications, not a trained world model or complete MPC controller.

## Example 1

Two scalar actions-1,+1, scores equal,all valid,E2,inverse_temperature 1,min_std 0,max_std 2 ->weights [.5,.5],mean 0,std 1.

## Example 2

Actions-1,+1,scores[0,log(3)],E2,inverse_temperature 1 ->eliteindices [1,0],weights [.75,.25],mean .5,std sqrt(.75). With max_std .5 ->std .5.
