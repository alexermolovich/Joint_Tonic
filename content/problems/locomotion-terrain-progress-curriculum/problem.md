# Sample Terrain Difficulty by Policy Progress

A terrain curriculum changes difficulty from measured progress rather than a generic success label. Promotion and demotion use different distance tests, and completing the highest level triggers a recorded reassignment.

## Contract

Levels integer(B,),0<=B<=16384,0<=level<num_levels; positions/origins real(B,2) world-frame horizontal meters abs<=1e4; commands real(B,2) horizontal robot-base-frame m/s abs<=100 (its speed norm is invariant to a horizontal yaw rotation); reset bool(B,); restart_draws real(B,) in[0,1). terrain_length scalar[1e-3,1e4] meters; episode_seconds scalar[1e-3,1000]seconds; num_levels built-in int1..1024. For resetting environments only, distance=norm(position-origin). move_up=distance>terrain_length/2; move_down=(distance<norm(command)*episode_seconds/2) AND NOT move_up. Candidate level=level+up-down. If >=num_levels, replace with floor(draw*num_levels); else clip at minimum0. Other levels unchanged. Return dict levels int64(B,), move_up/move_down/reassigned bool(B,), distance float64(B,) for all environments. Supplied draws replace official random reassignment to make replay deterministic; this is subsequent-reset curriculum only (initial reset is caller responsibility). Does not generate terrain geometry or update origin lookup; no direction-of-travel success claim. Promotion takes precedence if both raw criteria would hold.

Unless a tighter bound is stated below, numeric array-like inputs must have real integer/floating dtype after `np.asarray`, be finite with absolute values <=1e6 and at most 1,000,000 entries. Boolean, complex, string and object numeric arrays are invalid; Boolean masks must have Boolean dtype. Integer arrays/scalars exclude booleans. All invalid inputs raise ValueError. Return new arrays, preserve inputs, and compute floating outputs in float64 on CPU. No automatic differentiation is required.

## Physical context and scope

Positions and terrain lengths use meters; velocities m/s; angular rates rad/s; contact forces N; durations seconds; normalized action and unit-gravity coordinates are dimensionless. Penalty terms retain the individual units stated in the contract. Each environment is independent. Supplied episode counters and reset flags refer to the same control transition. Terrain update occurs on subsequent resets; no wall-clock scheduling or simulator action is performed. Bounded component associated with Learning to Walk in Minutes. Released reward/termination/curriculum formulas are isolated from full PPO training, physics, command randomization and hardware transfer. Supplied initialization states and recorded draws make replay deterministic.


## Example 1

levels[0,2],positions[[6,0],[6,0]],origins0,command[[1,0],[1,0]],resetallTrue,length10,seconds10,num_levels3,draws[0,.4] -> move_up[True,True],move_downFalse,levels[1,1],reassigned[False,True],distance[6,6].

## Example 2

level0,position[0,0],origin0,command[1,0],resetTrue,length10,seconds10,num_levels3,draw0 -> move_downTrue but output level0. At distance exactly5, both strict tests are false and level is unchanged.
