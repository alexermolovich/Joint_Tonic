# Roll Out Imagined Latent Trajectories

Start imagination from one known latent state and propagate using actions and learned dynamics only. This small supplied model makes the information boundary visible without pretending to reproduce a full recurrent stochastic model.

## Contract

```python
def imagine_latents(initial_state, actions, state_weight, action_weight, bias, reward_weight, reward_bias, continue_weight, continue_bias):
    ...
```

initial_state real(B,D), actions real(B,H,A), state_weight real(D,D),action_weight real(A,D),bias/reward_weight/continue_weight real(D,),reward_bias/continue_bias scalar[-10,10];1<=B<=32,0<=H<=64,1<=D,A<=32; all array entries abs<=10. Supplied actions normalized dimensionless. Original deterministic surrogate h[t+1]=tanh(h[t]@state_weight+actions[t]@action_weight+bias); reward[t]=h[t+1]@reward_weight+reward_bias; continuation[t]=stable_sigmoid(h[t+1]@continue_weight+continue_bias). Return dict states float64(B,H+1,D) including initial, rewards float64(B,H), continuation float64(B,H). No posterior observations are available after initialization; no stopping or zeroing when continuation is low (it is a prediction for return weighting). This is a supplied deterministic tanh dynamics teaching block, NOT Dreamer's RSSM/categorical sampling, trained world model, actor optimization or complete robot simulation. Preserve inputs and support zero horizon.

Unless a tighter bound is stated below, numeric array-like inputs must have real integer/floating dtype after `np.asarray`, be finite with absolute values <=1e6 and at most 1,000,000 entries. Boolean, complex, string and object numeric arrays are invalid; Boolean masks must have Boolean dtype. Integer arrays/scalars exclude booleans. All invalid inputs raise ValueError. Return new arrays, preserve inputs, and compute floating outputs in float64 on CPU. No automatic differentiation is required.

## Physical context and scope

Latents and normalized actions are dimensionless. Rewards/values use a fixed caller-declared dimensionless reward scale; KL is measured in nats. Each ordered index is one fixed caller-declared control interval. Predicted continuation is a probability, not an elapsed duration. No implicit frame conversion. A bounded component with supplied tensors. Prediction loss inputs and deterministic imagined dynamics do not reproduce the complete trained recurrent stochastic world model, actor or benchmark.

## Example 1

One state 0,action 0,all weights/biases0,H=1 -> states[[[0],[0]]],reward [[0]],continuation [[.5]].

## Example 2

State0, action 1, state_weight 0,action_weight 1,bias 0,reward_weight 2,reward_bias 1,continue_weight 0,continue_bias 0 -> next state tanh(1),reward 2*tanh(1)+1,continuation .5.
