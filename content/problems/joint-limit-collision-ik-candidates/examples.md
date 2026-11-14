## Worked examples

1. `lengths=[1,1], candidates=[[0,0],[pi/2,0]], joint_limits=[[-pi,pi],[-pi,pi]], obstacles=empty((0,3)), target=[2,0], margin=0` selects index0, q `[0,0]`, point `[2,0]`, error0.
2. Add obstacle `[0.5,0,0.1]`. Candidate0 crosses it, so select index1 with point approximately `[0,2]` and error `sqrt(8)`.
