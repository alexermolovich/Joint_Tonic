# Roll Out a Latent Dynamics Sequence

Planning repeatedly feeds a predicted latent into the next transition. Keep each predicted state on the same groupwise simplex as the initial representation instead of drifting into unconstrained coordinates.

## Contract

```python
def latent_sequence(initial_state, actions, state_weight, action_weight, bias, group_size):
    ...
```

initial_state real(B,D),actions real(B,H,A),state_weight real(D,D),action_weight real(A,D),bias real(D,),group_size built-in int1..32 dividing D. 1<=B<=32,0<=H<=64,1<=D,A<=32; parameter/action values abs<=10. Initial state entries must be nonnegative, each consecutive group sum1 within atol1e-9/rtol0. At every step raw=z@state_weight+action@action_weight+bias; nextz=stable grouped softmax(raw). Return fresh float64(B,H+1,D), including exact initial state. Supplied affine transition followed by actual SimNorm is an original deterministic teaching surrogate for the learned multi-layer TD-MPC2 dynamics. It is not Dreamer's tanh recurrence, latent stochastic sampling or observation re-encoding.

Unless a tighter bound is stated below, numeric array-like inputs must have real integer/floating dtype after `np.asarray`, be finite with absolute values <=1e6 and at most 1,000,000 entries. Boolean, complex, string and object numeric arrays are invalid; Boolean masks must have Boolean dtype. Integer arrays/scalars exclude booleans. All invalid inputs raise ValueError. Return new arrays, preserve inputs, and compute floating outputs in float64 on CPU. No automatic differentiation is required.

## Physical context and scope

Latents and normalized commands are dimensionless. Rewards and decoded critic values share the declared dimensionless score scale; inverse temperature has reciprocal score units. Each horizon index is one fixed caller-declared control interval. Termination occurs after the current transition reward. No implicit frame conversion or simulator execution. Bounded component informed by TD-MPC2 and the pinned official implementation. Affine dynamics and deterministic supplied critic/candidate inputs are declared teaching simplifications, not a trained world model or complete MPC controller.

## Example 1

state [[.5,.5]],actions[[[0]]],all weights/bias 0,group 2 ->two identical states [.5,.5].

## Example 2

Same initial state,action 1,action_weight [[0,log(3)]],other weights 0 ->next state [.25,.75].
