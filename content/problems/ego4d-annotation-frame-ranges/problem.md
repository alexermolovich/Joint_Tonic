# Align Egocentric Video Annotations

## Contract

annotation_frame_ranges(frame_times_ns, intervals_ns) -> ndarray. frame_times_ns int64(T,),0<=T<=1000000, nonnegative strictly increasing on one source-video clock. intervals_ns int64(A,2),0<=A<=100000, nonnegative start<end. Treat annotations as half-open [start,end) intervals; return int64(A,2) frame-index ranges[lo,hi) containing timestamps start<=t<end, using insertion positions. Intervals can overlap or lie outside video coverage; empty matches return equal insertion indices, not(-1,-1). Preserve input interval order. No constant-frame-rate assumption; no exposure integration or temporal-IoU metric. Inputs belong to one source video; multi-video identity must be handled before calling.

## Input rules

All tasks are original bounded CPU teaching components. NumPy arrays must have exactly the documented dtype and shape, support noncontiguous layout and remain unchanged; returned containers are fresh. Floating arrays use float32/float64 and outputs float64 unless stated otherwise. Integer arrays use int64 and Boolean arrays bool. Invalid arguments raise ValueError unless a task explicitly returns a report; built-in integer scalars exclude bool. Exact identifier strings match [a-z][a-z0-9_-]{0,31}. Physical units, time axes, zero-evidence behavior and missing-data masks are explicit per task. Runtime Python3.12.3/NumPy2.2.4, original synthetic CC0 fixtures; no network or wall-clock access. These are not reproductions of paper headline results or released dataset loaders.

## Worked examples

### Example 1

frame_times[0,10,25,40],intervals[[10,40],[11,24],[50,60]] -> [[1,3],[2,2],[4,4]].

### Example 2

empty timestamps and intervals[[0,1]] -> [[0,0]].

## Source and scope

Original bounded component associated with [2021-ego4d](https://arxiv.org/abs/2110.07058). It does not reproduce the full dataset loader, task suite or headline results.
