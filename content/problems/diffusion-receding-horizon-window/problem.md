# Execute a Receding-Horizon Action Window

Implement receding_horizon_window(trajectory, valid, offset, execute_steps), returning a fresh copy of shape (B,execute_steps,D).

trajectory is a float32/float64 NumPy array (B,H,D), finite with abs(value)<=1e6. Require 1<=B<=64,1<=H<=256,1<=D<=64, and <=2,000,000 elements. valid is a bool NumPy array (B,H). offset and execute_steps are built-in non-bool ints; 0<=offset<H,1<=execute_steps<=H,offset+execute_steps<=H.

Copy trajectory[:,offset:offset+execute_steps,:] preserving dtype, order, units and coordinate frame. Every selected validity entry must be True; otherwise raise ValueError for the entire batch. Invalid entries outside the selected window are allowed, but all trajectory values must still satisfy finiteness/range. Do not skip holes, shorten the requested window, extrapolate, repeat the last action or zero invalid selected commands. Noncontiguous inputs are supported. Never mutate inputs or return an alias.

Raise TypeError for non-array trajectory/valid or invalid integer types. Raise ValueError for every array-contract, range or selected-validity violation. Each batch item is one already-aligned observation with a fixed controller period; offset is a discrete tick count, not seconds. Caller supplies physical channel conventions. No quaternion averaging, actuator safety checking or actual execution is performed.

## Source and scope

Extract the controller-supported prefix of a predicted future trajectory after a specified alignment offset. This returns a command buffer for a synthetic controller; it does not drive a robot, run denoising or infer the observation-horizon offset.

[Primary paper](https://arxiv.org/abs/2303.04137).


## Worked examples

### Execute only a near-term segment

trajectory=[[[10],[20],[30],[40]]], valid=[[True,True,True,True]], offset=1, execute_steps=2.

Return [[[20],[30]]]. The next observation may replace the rest of the plan; the final40 is not queued by this call.

### Padding outside the selected window

trajectory=[[[1,2],[3,4],[0,0]]], valid=[[True,True,False]], offset=0, execute_steps=2.

Return [[[1,2],[3,4]]]. Asking instead for offset=1,execute_steps=2 raises ValueError, because the selected tail includes unavailable target data.


## Hints

1. Validate the requested index range before slicing.
2. Check all selected validity entries; any false entry rejects the window.
3. Copy the slice so later replanning cannot mutate an already returned buffer.


## Runtime and tolerances

Python 3.12.3; NumPy 2.2.4. Shared worker limits: 18 seconds wall time, 10 seconds CPU, 4096 MiB memory and 64 KiB output. Numerical comparisons use rtol=1e-6 and atol=1e-7 unless an exact boolean/integer result is specified. Synthetic fixtures are CC0-1.0.
