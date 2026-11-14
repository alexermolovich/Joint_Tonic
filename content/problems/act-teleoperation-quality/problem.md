# Detect Teleoperation Demonstration Quality Failures

A demonstration can look smooth in video while its logged joint stream contains impossible jumps or missing observations. Separate these failure types so a curator can inspect the evidence rather than discarding an entire dataset blindly.

## Contract

`teleop_quality_flags(times,joints,observed,lower,upper,max_speed)` receives strictly increasing finite times(T,) in seconds, 1<=T<=4096; finite joints(T,D),1<=D<=64 in radians; observed:bool(T,); lower/upper/max_speed:(D,), lower<upper and max_speed>0. Return dict missing:bool(T,) = ~observed, out_of_range:bool(T,) for any joint outside inclusive limits, speed_jump:bool(T,) for any absolute finite difference divided by dt exceeding max_speed. speed_jump[0]=False. Evaluate range and speed on all rows independently of observed; observed only marks sensor completeness. Inputs can exceed the supplied joint ranges because finding those rows is the task.

Unless a tighter bound is stated below, numeric array-like inputs must have real integer/floating dtype after `np.asarray`, be finite with absolute values <=1e6 and at most1,000,000 entries. Boolean, complex, string and object numeric arrays are invalid; Boolean masks must have Boolean dtype. Integer arrays/scalars exclude booleans. All invalid inputs raise ValueError. Return new arrays, preserve inputs, and compute floating outputs in float64 on CPU. No automatic differentiation is required.

## Physical context and scope

Joint positions radians; times seconds; max_speed radians/second, one threshold per joint. Time samples must be strictly increasing on one clock; differences are between adjacent recorded rows. Original demonstration-quality check motivated by ALOHA/ACT data collection. Thresholds are supplied; this is not a collision or contact-quality evaluator.


## Example 1

times=[0,1], joints=[[0],[2]], observed=[True,False], lower=[-1], upper=[1], max_speed=[1] returns missing=[False,True], out_of_range=[False,True], speed_jump=[False,True].

## Example 2

times=[0,0.5], joints=[[0],[1]], both observed, range[-1,1], max_speed=[2] returns all False. Equality at the range and speed thresholds is valid.
