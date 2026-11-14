# Solve IK with a Jacobian Pseudoinverse

Iteratively solve planar two-link position IK using a bounded pseudoinverse update.

```python
def solve_planar_ik(lengths, initial_q, target, max_iterations, tolerance, max_step):
```

## Contract

Lengths positive. max_iterations is integer 0..200, not bool. tolerance and max_step are positive scalar values. At each state, record Euclidean endpoint error. Stop if error<=tolerance or all updates are used. Otherwise compute dq=pinv(J,rcond=1e-12)@(target-endpoint), scale dq only if its norm exceeds max_step, and add it to q. Return final q without wrapping, convergence bool, and error history containing initial plus every updated state (length 1..max_iterations+1). No joint limits, collision tests, damping, line search, or restarts.

**Shapes and outputs:** lengths(2,), initial_q(2,), target(2,), scalar controls -> (float64 q(2,), bool converged, float64 errors(K,)).

**Units:** lengths,target: metres, angles,max_step: radians, tolerance: metres. **Time:** Static target; iterations are numerical steps, not physical timesteps.

Numeric inputs are converted with np.asarray and must then have integer or floating dtype (CPU). Boolean, string, complex, and object dtypes are rejected; mixed lists follow NumPy coercion. NaN/Inf and magnitudes above 1e9 raise ValueError. Other contract violations also raise ValueError. Do not mutate inputs. Outputs are new arrays unless stated otherwise. Numerical tolerance: rtol=1e-7, atol=1e-9. Runtime: Python 3.12.3, NumPy 2.2.4; 18 s wall, 10 s CPU, 4096 MiB address space, 64 KiB output. Fixtures are original synthetic CC0-1.0 data.

## Worked examples

1. `lengths=[1,1], initial_q=[0,pi/2], target=[1,1], max_iterations=20, tolerance=1e-6, max_step=0.5` returns the initial q, True, and a one-element near-zero error history.
2. `lengths=[1,1], initial_q=[0,0], target=[3,0], max_iterations=2, tolerance=1e-6, max_step=0.5` returns `[0,0]`, False, errors `[1,1,1]`; the straight arm cannot move outward.

Each link length must be at least 1e-9 metres; smaller values raise ValueError.
