# Rank Multi-Seed Motion Trajectories

Implement `rank_trajectories(endpoint_error, collision_free, limits_ok, objective, endpoint_tolerance)`.

Rank supplied motion candidates after explicit feasibility gates.

`endpoint_error` and `objective` are nonnegative float64 `(N,)`, `0<=N<=100000`. `collision_free` and `limits_ok` are bool `(N,)`. `endpoint_tolerance` is a Python int/float in `[0,1e6]`. Errors use one normalized endpoint-distance convention; objectives use one common normalized cost. All candidates describe the same start/goal task and validation setup.

A candidate is eligible exactly when both supplied flags are True and endpoint_error<=endpoint_tolerance. Return a dictionary with fresh bool `feasible (N,)`, int64 `order (F,)` containing only eligible indices sorted by `(objective,index)`, and Python int `best`, the first ordered index or -1 when none are eligible. Endpoint equality passes; exact cost ties keep the original index order. Empty input is valid. Flags summarize caller-performed validation, which may be sampled; they do not establish continuous collision freedom. This selection component neither optimizes trajectories nor runs cuRobo.

## Validation and runtime

All array arguments must be NumPy arrays with the stated rank and dtype: real arrays use float64, index arrays int64, masks bool. Real entries must be finite with absolute value at most 1e6 unless a tighter range is stated. All malformed types, shapes, ranges, or scalar arguments raise ValueError. Support noncontiguous arrays, preserve every input, and return fresh arrays (no input storage alias). CPU only; no implicit batch dimension. Comparisons use rtol=1e-6 and atol=1e-7. Fixtures are original synthetic data (CC0-1.0).

## Worked examples

1. Errors `[0.1,0.2,0.05]`, both flags all True, objectives `[3.,1.,3.]`, tolerance `0.1` give feasible `[True,False,True]`, order `[0,2]`, best `0`.
2. Errors `[0.]`, collision flag `[False]`, limits flag `[True]`, objective `[0.]`, tolerance `0` give feasible `[False]`, empty int64 order and best `-1`.

## Source and scope

[Primary source](https://arxiv.org/abs/2310.17274). This isolates the stated component using synthetic fixtures; completing it does not reproduce the full paper.
