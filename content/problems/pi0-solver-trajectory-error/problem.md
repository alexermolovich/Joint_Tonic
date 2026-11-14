# Evaluate Solver Steps Against Trajectory Error

More solver steps spend time without guaranteeing a better predicted trajectory. Compare final chunks against one declared reference, then choose a candidate using measured latency only after its error satisfies the required limit.

## Contract

estimates real(K,H,D),1<=K<=64,1<=H<=256,1<=D<=32; target real(H,D), steps integer(K,) strictlypositive<=10000 (duplicates allowed), latency_ms real(K,) nonnegative. max_rmse/deadline_ms real scalars0..1e6. Each candidate is a FINAL action chunk from a supplied solver step count, not an intermediate flow state. Return rmse float64(K,) over H*D, max_abs_error float64(K,), feasible bool(K,) requiring RMSE<=max_rmse and latency<=deadline, selected_index Pythonint: among feasible candidates minimize latency, then steps, then originalindex; -1 if none. No model inference or claim that more steps always improves output.

Unless a tighter bound is stated below, numeric array-like inputs must have real integer/floating dtype after `np.asarray`, be finite with absolute values <=1e6 and at most1,000,000 entries. Boolean, complex, string and object numeric arrays are invalid; Boolean masks must have Boolean dtype. Integer arrays/scalars exclude booleans. All invalid inputs raise ValueError. Return new arrays, preserve inputs, and compute floating outputs in float64 on CPU. No automatic differentiation is required.

## Physical context and scope

Actions are normalized dimensionless; error same units; measured solver latency and deadline milliseconds; flow step count dimensionless. Caller-synchronized observations; generation time and physical control time are distinct. Original bounded engineering component motivated by the paper; no pretrained model or benchmark reproduction is implied.


## Example 1

estimates=[[[1]],[[0]]],target=[[0]],steps=[1,4],latencies=[2,4],max_rmse=.5,deadline4 returns rmse[1,0],max_abs[1,0],feasible[False,True],selected_index1.

## Example 2

For two exact candidates, steps=[4,2], latencies=[3,3], errorlimit0,deadline3, choose index1 (fewer steps at equal latency).
