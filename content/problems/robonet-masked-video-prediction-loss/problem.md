# Compute a Masked Video-Prediction Loss

## Contract

masked_video_loss(predicted,target,valid) -> dict{loss,per_horizon,frame_counts,has_data}. predicted/target float(B,T,H,W,C) same shape,0<=B<=256,1<=T<=256,1<=H,W<=64,C in{1,3},total entries<=1e6. valid bool(B,T). At valid frames all pixels must finite[0,1]; invalid frames may contain arbitrary finite/NaN/Inf placeholders and are completely ignored. Per-frame MSE averages ALL HWC pixel/channel squared differences; loss averages over all valid frames, not equally over horizons. per_horizon float64(T,) averages valid frames at each horizon, NaN when none; frame_counts int64(T,); has_data Python bool. If no data, loss0,has_dataFalse,all per_horizonNaN. This simple normalized-pixel regression is an original bounded teaching objective, not all RoboNet model losses or a perceptual quality score.

## Input rules

All tasks are original bounded CPU teaching components. NumPy arrays must have exactly the documented dtype and shape, support noncontiguous layout and remain unchanged; returned containers are fresh. Floating arrays use float32/float64 and outputs float64 unless stated otherwise. Integer arrays use int64 and Boolean arrays bool. Invalid arguments raise ValueError unless a task explicitly returns a report; built-in integer scalars exclude bool. Exact identifier strings match [a-z][a-z0-9_-]{0,31}. Physical units, time axes, zero-evidence behavior and missing-data masks are explicit per task. Runtime Python3.12.3/NumPy2.2.4, original synthetic CC0 fixtures; no network or wall-clock access. These are not reproductions of paper headline results or released dataset loaders.

## Worked examples

### Example 1

B1,T2,H1,W2,C1: target valid firstframe[0,1],prediction[.2,.8],secondframe padded; valid[[True,False]] -> loss.04,per_horizon[.04,NaN],counts[1,0],has_dataTrue.

### Example 2

B2,T2,one-pixel target0; prediction[[0,1],[1,NaN]],valid[[True,True],[True,False]] -> loss2/3,per_horizon[.5,1],counts[2,1].

## Source and scope

Original bounded component associated with [2019-robonet](https://arxiv.org/abs/1910.11215). It does not reproduce the full dataset loader, task suite or headline results.
