# Align Tactile Frames with Robot Actions

A frame must be paired with a command that was already active when the image was captured. A future command can be closer in absolute time and still be the wrong cause of the observed contact.

## Contract

`frame_times` is real `(N,)`, `action_times` is real `(M,)` and `actions` is real `(M, D)`, where `0 <= N, M <= 4096` and `1 <= D <= 16`. Times lie in `[0, 1_000_000]` seconds on one clock. Action timestamps increase strictly; frame queries may be unsorted. Commands lie in `[-1, 1]` and use a fixed normalized controller-channel order. `max_age` is a scalar in `[0, 100]` seconds.

For each frame, choose the latest action timestamp less than or equal to the frame timestamp. Return a dictionary with `indices` (int64 `(N,)`, chosen predecessor or -1 if absent), `age` (float64 `(N,)`, frame minus action time, or NaN if absent), `valid` (Boolean `(N,)`, candidate exists and age is at most the limit), and `aligned` (float64 `(N, D)`, selected command if valid, otherwise zero).

A stale predecessor retains its index and age for diagnosis, but its aligned command is zero. Empty action streams produce all-invalid results. This is a causal zero-order hold; do not select future commands, interpolate, compensate dynamics or estimate clock offsets.

Unless a tighter bound is stated below, numeric array-like inputs must have real integer/floating dtype after `np.asarray`, be finite with absolute values <=1e6 and at most 1,000,000 entries. Boolean, complex, string and object numeric arrays are invalid; Boolean masks must have Boolean dtype. Integer arrays/scalars exclude booleans. All invalid inputs raise ValueError. Return new arrays, preserve inputs, and compute floating outputs in float64 on CPU. No automatic differentiation is required.

## Physical context and scope

Image intensities and normalized commands are dimensionless. Image coordinates use integer pixel centers with x right and y down. Time is seconds except explicitly microsecond exposure metadata. One sensor and aligned optical calibration; action timestamps share the sensor clock. No implicit clock or physical-frame conversion. Original operational or vision diagnostic motivated by DIGIT. It is not the paper's reconstruction/controller implementation, calibrated force, or proof of contact safety.

## Example 1

Action times [0, 1], commands [[0.2], [0.8]], frame times [0.5, 1] and max_age 0.5 yield indices [0, 1], ages [0.5, 0], both valid, and aligned commands [[0.2], [0.8]].

## Example 2

With one action at time 1 and frames at [0.5, 2], max_age 0.5 yields indices [-1, 0], ages [NaN, 1], both invalid, and zero aligned commands.
