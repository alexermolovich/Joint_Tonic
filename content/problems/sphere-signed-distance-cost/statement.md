# Compute a Signed-Distance Collision Cost

Implement `sphere_collision_cost(centers, radii, obstacles, obstacle_radii, margin)`.

Score a batch of robot sphere approximations against spherical obstacles in one world frame.

`centers` is float64 `(B,S,3)`, `1<=B<=64`, `1<=S<=32`; `radii` float64 `(S,)`; `obstacles` float64 `(K,3)` and `obstacle_radii` float64 `(K,)`, `1<=K<=32`. All positions/radii are meters in the same right-handed world frame at one scene timestamp, and all radii are >=1e-9. `margin` is Python int/float in `[0,100]` meters. Sphere-pair separation is `d=norm(center-obstacle)-radius-obstacle_radius`, positive outside contact. Return fresh arrays `cost` float64 `(B,)`: sum of squared hinges `max(margin-d,0)²` over all sphere pairs; `clearance` float64 `(B,)`: minimum pair separation; `collision` bool `(B,)`: any pair with d<=0. Contact counts as collision even when margin0 produces zero hinge cost. This original sphere-sphere surrogate does not implement cuRobo's complete collision kernels or guarantee safety of a full robot mesh.

## Validation and runtime

All array arguments must be NumPy arrays with the stated rank and dtype: real arrays use float64, index arrays int64, masks bool. Real entries must be finite with absolute value at most 1e6 unless a tighter range is stated. All malformed types, shapes, ranges, or scalar arguments raise ValueError. Support noncontiguous arrays, preserve every input, and return fresh arrays (no input storage alias). CPU only; no implicit batch dimension. Comparisons use rtol=1e-6 and atol=1e-7. Fixtures are original synthetic data (CC0-1.0).

## Worked examples

1. One robot sphere centered at `(0,0,0)` meters with radius 1, one obstacle at `(3,0,0)` radius 1, margin 2: clearance 1 m, cost 1 m², collision False.
2. Move the obstacle to `(2,0,0)` and set margin0: clearance zero, cost zero, collision True because the spheres touch.

## Source and scope

[Primary source](https://arxiv.org/abs/2310.17274). This isolates the stated component using synthetic fixtures; completing it does not reproduce the full paper.
