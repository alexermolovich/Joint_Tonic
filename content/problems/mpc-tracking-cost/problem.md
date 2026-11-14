# Evaluate an MPC Tracking Cost

Score a finite-horizon predicted trajectory with stage, control-effort, and terminal penalties.

```python
def mpc_tracking_cost(states, targets, controls, state_weights, control_weights, terminal_weights):
```

## Contract

D,M>=1; N may be zero. Weight vectors are nonnegative and represent diagonal quadratic penalties. Sum state tracking errors at k=0..N-1 and controls at k=0..N-1; apply terminal_weights only to final state k=N. Targets have exactly the same shape as states. No terminal double-counting or timestep factor.

**Shapes and outputs:** states/targets(N+1,D), controls(N,M), state_weights/terminal_weights(D,), control_weights(M,) -> Python float.

**Units:** states,targets: declared state units, controls: declared actuator units, weights: inverse squared corresponding units, cost: dimensionless. **Time:** State rows 0..N; control row k applies between states k and k+1, with no dt multiplier in this discrete objective.

Numeric inputs are converted with np.asarray and must then have integer or floating dtype (CPU). Boolean, string, complex, and object dtypes are rejected; mixed lists follow NumPy coercion. NaN/Inf and magnitudes above 1e9 raise ValueError. Other contract violations also raise ValueError. Do not mutate inputs. Outputs are new arrays unless stated otherwise. Numerical tolerance: rtol=1e-7, atol=1e-9. Runtime: Python 3.12.3, NumPy 2.2.4; 18 s wall, 10 s CPU, 4096 MiB address space, 64 KiB output. Fixtures are original synthetic CC0-1.0 data.

## Worked examples

1. `states=[[1],[2],[3]], targets=zeros((3,1)), controls=[[1],[2]], state_weights=[1], control_weights=[2], terminal_weights=[3]` → `42.0`.
2. `states=[[2,-1]], targets=[[0,0]], controls=empty((0,1)), state_weights=[9,9], control_weights=[1], terminal_weights=[2,3]` → `11.0`.
