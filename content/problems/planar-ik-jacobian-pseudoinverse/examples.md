## Worked examples

1. `lengths=[1,1], initial_q=[0,pi/2], target=[1,1], max_iterations=20, tolerance=1e-6, max_step=0.5` returns the initial q, True, and a one-element near-zero error history.
2. `lengths=[1,1], initial_q=[0,0], target=[3,0], max_iterations=2, tolerance=1e-6, max_step=0.5` returns `[0,0]`, False, errors `[1,1,1]`; the straight arm cannot move outward.
