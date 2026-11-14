# Build Lambda-Return Targets

An imagined transition may continue only with some predicted probability. Multiply the bootstrapped future by that probability while preserving the immediate reward and a clear final-step bootstrap.

## Contract

```python
def imagined_lambda_returns(rewards, next_values, continuation, valid, gamma, lam):
    ...
```

rewards, next_values, continuation real(B,T), valid Boolean same shape;1<=B<=64,1<=T<=1024; rewards/values abs<=1e6,continuation[0,1], gamma/lam scalar[0,1]. Validity forms prefix per row (possibly empty). next_values[t] is value at transition t's successor latent state; continuation[t] is predicted probability of continuing through that transition. In reverse, recursive_next is G[t+1] when next slot valid, otherwise next_values[t]; G[t]=r[t]+gamma*c[t]*((1-lam)*next_values[t]+lam*recursive_next). Return float64(B,T), zero invalid. Every invalid-mask numeric input still validated. Last valid step bootstraps its successor value. This explicit next-state indexing distinguishes the task from some paper notation. Fractional predicted continuation is essential; existing PPO Boolean terminal/truncation task is only a prerequisite.

Unless a tighter bound is stated below, numeric array-like inputs must have real integer/floating dtype after `np.asarray`, be finite with absolute values <=1e6 and at most 1,000,000 entries. Boolean, complex, string and object numeric arrays are invalid; Boolean masks must have Boolean dtype. Integer arrays/scalars exclude booleans. All invalid inputs raise ValueError. Return new arrays, preserve inputs, and compute floating outputs in float64 on CPU. No automatic differentiation is required.

## Physical context and scope

Latents and normalized actions are dimensionless. Rewards/values use a fixed caller-declared dimensionless reward scale; KL is measured in nats. Each ordered index is one fixed caller-declared control interval. Predicted continuation is a probability, not an elapsed duration. No implicit frame conversion. A bounded component with supplied tensors. Prediction loss inputs and deterministic imagined dynamics do not reproduce the complete trained recurrent stochastic world model, actor or benchmark.

## Example 1

rewards[[1,2]],next_values[[10,20]],continuation[[.5,1]],valid all,gamma .5, lam 1 => last 12, first 4.

## Example 2

Same values with lam 0 =>[3.5,12]; with first continuation 0 =>first 1 regardless of successor target.
