# Reset Failed Locomotion Environments

Reset logic should identify why an episode ended before replacing state. A timeout and a forbidden body contact both restart an environment, but downstream value targets may treat them differently.

## Contract

Contact force real(B,K,3) Newtons,0<=B<=4096,0<=K<=16 (caller-selected termination contact bodies),abs<=1e4. Episode steps integer(B,)0..1e6; max_steps built-in int1..1e6. State/initial real(B,D),1<=D<=64, abs<=1e4, caller-declared matched units and frame. last_action real(B,A),1<=A<=32 normalized[-1,1]; feet_air_time real(B,F),1<=F<=8 seconds[0,100]. Failure any selected body Euclidean force norm>1 N; timeout episode_steps>max_steps (strict released convention). Reset=failure OR timeout. Return dict failure,timeout,reset bool(B,), state float64(B,D) from initial where reset else state, last_action and feet_air_time with reset rows zeroed, episode_steps int64(B) reset to0. Empty K produces no contact failures. Both failure and timeout can be true; preserve both. Reset states supplied deterministically, no command randomization, controller actuation or episode-version increment. Generic selective reset exercise remains prerequisite; this adds locomotion termination signals and action/contact history clearing.

Unless a tighter bound is stated below, numeric array-like inputs must have real integer/floating dtype after `np.asarray`, be finite with absolute values <=1e6 and at most 1,000,000 entries. Boolean, complex, string and object numeric arrays are invalid; Boolean masks must have Boolean dtype. Integer arrays/scalars exclude booleans. All invalid inputs raise ValueError. Return new arrays, preserve inputs, and compute floating outputs in float64 on CPU. No automatic differentiation is required.

## Physical context and scope

Positions and terrain lengths use meters; velocities m/s; angular rates rad/s; contact forces N; durations seconds; normalized action and unit-gravity coordinates are dimensionless. Penalty terms retain the individual units stated in the contract. Each environment is independent. Supplied episode counters and reset flags refer to the same control transition. Terrain update occurs on subsequent resets; no wall-clock scheduling or simulator action is performed. Bounded component associated with Learning to Walk in Minutes. Released reward/termination/curriculum formulas are isolated from full PPO training, physics, command randomization and hardware transfer. Supplied initialization states and recorded draws make replay deterministic.


## Example 1

B2,K1 contacts[[[1,0,0]],[[0,1.01,0]]], steps[5,5],max5, state[[2],[3]],initial[[0],[1]],last_action[[.2],[.3]],feet[[.1],[.2]] -> failure[False,True],timeout[False,False],reset[False,True],state[[2],[1]],last_action[[.2],[0]],feet[[.1],[0]],steps[5,0].

## Example 2

zero selected contact bodies, one environment steps6,max5 -> failureFalse,timeoutTrue,resetTrue and the same reset/history-clearing behavior. Timeouts remain separately reported for downstream bootstrap handling.
