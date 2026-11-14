# Score Candidate Action Trajectories

A candidate plan earns predicted rewards until its first terminal transition. Its terminal critic estimate contributes only if the complete planned horizon remains alive.

## Contract

```python
def score_latent_trajectories(rewards, terminated, terminal_values, gamma):
    ...
```

rewards real(K,H),terminated bool(K,H),terminal_values real(K,),gamma scalar[0,1];1<=K<=1024,0<=H<=128;absvalues<=1e6. Reward at step t occurs before terminated[t] ends that transition. Define alive initiallyTrue, weight[t]=gamma**t if all previous terminatedflagsFalse else0. Return dict contributions float64(K,H)=weight*reward; tail float64(K)=gamma**H*terminal_value if no termination in horizon else0; scores float64(K)=sum contributions+tail; best Pythonint argmax(scores),tie lowestindex. Any later rewards after first termination ignored but still numerically validated. With H0 score=terminal_value. Values already decoded from model predictions; no neural inference occurs here. This explicit Boolean termination extension matches current official episodic planner convention, not a claim about every2023 configuration.

Unless a tighter bound is stated below, numeric array-like inputs must have real integer/floating dtype after `np.asarray`, be finite with absolute values <=1e6 and at most 1,000,000 entries. Boolean, complex, string and object numeric arrays are invalid; Boolean masks must have Boolean dtype. Integer arrays/scalars exclude booleans. All invalid inputs raise ValueError. Return new arrays, preserve inputs, and compute floating outputs in float64 on CPU. No automatic differentiation is required.

## Physical context and scope

Latents and normalized commands are dimensionless. Rewards and decoded critic values share the declared dimensionless score scale; inverse temperature has reciprocal score units. Each horizon index is one fixed caller-declared control interval. Termination occurs after the current transition reward. No implicit frame conversion or simulator execution. Bounded component informed by TD-MPC2 and the pinned official implementation. Affine dynamics and deterministic supplied critic/candidate inputs are declared teaching simplifications, not a trained world model or complete MPC controller.

## Example 1

rewards[[1,2]],no termination,terminal 4,gamma .5 ->contributions [1,1],tail 1,score 3.

## Example 2

Same row terminated[True,False] ->contributions [1,0],tail 0,score 1.
