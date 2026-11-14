# Measure Cross-Robot Prediction Error

## Contract

cross_robot_prediction_error(robot_ids,episode_ids,squared_error,pixel_counts) -> dict{robot_ids,episode_counts,pixel_counts,pixel_mse,episode_mse}. Four vectors shape(N,),0<=N<=100000. IDs/counts int64 nonnegative; pixel_counts each0..1e9. squared_error float(N,) finite[0,1e9], an already-summed squared residual over normalized pixel/channel samples; require squared_error<=pixel_counts, and if count0 require error0. episode IDs unique within robot namespace; repeated(robot,episode) rows are chunks of same episode and aggregate. A zero-pixel chunk contributes no evidence. Include all declared robot IDs even if all counts0. For each sorted robot, pixel_mse=totalerror/totalpixels; episode_mse=equal mean of per-episode(error/pixels) among positive-pixel episodes. episode_counts counts those observed episodes; output counts int64, metricsfloat64 with NaN when no evidence. Different robot IDs sharing episode ID do not merge. This exposes weighting effects and missing support without classifying train/test robots or making transfer-causality claims.

## Input rules

All tasks are original bounded CPU teaching components. NumPy arrays must have exactly the documented dtype and shape, support noncontiguous layout and remain unchanged; returned containers are fresh. Floating arrays use float32/float64 and outputs float64 unless stated otherwise. Integer arrays use int64 and Boolean arrays bool. Invalid arguments raise ValueError unless a task explicitly returns a report; built-in integer scalars exclude bool. Exact identifier strings match [a-z][a-z0-9_-]{0,31}. Physical units, time axes, zero-evidence behavior and missing-data masks are explicit per task. Runtime Python3.12.3/NumPy2.2.4, original synthetic CC0 fixtures; no network or wall-clock access. These are not reproductions of paper headline results or released dataset loaders.

## Worked examples

### Example 1

robot[0,0],episode[1,2],error[1,0],pixels[1,9] -> robot0 episodes2,pixels10,pixel_mse.1,episode_mse.5.

### Example 2

robot[2],episode[8],error[0],pixels[0] -> robot2 episodes0,pixels0,botherrorsNaN.

## Source and scope

Original bounded component associated with [2019-robonet](https://arxiv.org/abs/1910.11215). It does not reproduce the full dataset loader, task suite or headline results.
