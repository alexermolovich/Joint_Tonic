## Worked examples

1. `initial_pose=[0,0,0], wheel_rates=[[1,1],[1,1]], dt=1, radius=1, track=2` → `[[0,0,0],[1,0,0],[2,0,0]]`.
2. Same parameters with one rate row `[[0,2]]` → final `[sin(1),1-cos(1),1]`, approximately `[0.84147098,0.45969769,1]`.
