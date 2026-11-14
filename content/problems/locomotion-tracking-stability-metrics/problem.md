# Compute Gait Tracking and Stability Metrics

Command tracking and body stability describe different parts of locomotion. Keep their terms separate so a good tracking reward cannot hide unwanted vertical motion or body tilt.

## Contract

Arrays velocity/angular/command/gravity real(B,T,3),0<=B<=128,1<=T<=256, abs<=100 except gravity unit vectors with norm1 atol1e-7. Commands columns desired base-frame vx,vy (m/s), yaw rate wz (rad/s); linear/angular measurements in same right-handed base frame with x forward,y left,z up. Projected gravity is the world unit downward vector expressed in body coordinates. Valid bool(B,T); scales positive [1e-6,1000] with linear_scale (m/s)^2 and yaw_scale (rad/s)^2. Per valid sample tracking errors ev=(vx-cx)^2+(vy-cy)^2 and ew=(wz-cw)^2; rewards exp(-ev/linear_scale),exp(-ew/yaw_scale). Stability diagnostics: vertical velocity squared vz^2 in(m/s)^2, roll/pitch angular rate squared wx^2+wy^2 in(rad/s)^2, tilt penalty gx^2+gy^2 dimensionless. Return dict per_step float64(B,T,5) ordered [linear_reward,yaw_reward,vertical_penalty,angular_penalty,tilt_penalty] with invalid zero; counts int64(B), means float64(B,5), NaN rows with no valid samples. No sum of unlike-unit penalties or configured reward weights/time-step factors. These scalar terms match released reward mechanisms; reporting masks/means are original diagnostics.

Unless a tighter bound is stated below, numeric array-like inputs must have real integer/floating dtype after `np.asarray`, be finite with absolute values <=1e6 and at most 1,000,000 entries. Boolean, complex, string and object numeric arrays are invalid; Boolean masks must have Boolean dtype. Integer arrays/scalars exclude booleans. All invalid inputs raise ValueError. Return new arrays, preserve inputs, and compute floating outputs in float64 on CPU. No automatic differentiation is required.

## Physical context and scope

Positions and terrain lengths use meters; velocities m/s; angular rates rad/s; contact forces N; durations seconds; normalized action and unit-gravity coordinates are dimensionless. Penalty terms retain the individual units stated in the contract. Each environment is independent. Supplied episode counters and reset flags refer to the same control transition. Terrain update occurs on subsequent resets; no wall-clock scheduling or simulator action is performed. Bounded component associated with Learning to Walk in Minutes. Released reward/termination/curriculum formulas are isolated from full PPO training, physics, command randomization and hardware transfer. Supplied initialization states and recorded draws make replay deterministic.


## Example 1

B=T=1, measured v[.8,.1,.2], w[.1,.2,.3], command[1,0,.5], gravity[0,0,-1], validTrue, scales .25,.25 -> terms [exp(-.2),exp(-.16),.04,.05,0], count1 and same means.

## Example 2

v=w=command0, gravity[1,0,0], validTrue -> [1,1,0,0,1]. ValidFalse gives all-zero terms,count0,all-NaN means. A perfectly upside-down gravity[0,0,1] also has zero tilt penalty; explicitly this surrogate alone cannot certify upright stability.
