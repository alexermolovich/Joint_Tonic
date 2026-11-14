# Track the Age of an Asynchronous Adaptation Latent

A newly completed adaptation job can still describe old observations. Track completion age separately from evidence age so a controller does not confuse computation availability with freshness.

## Contract

`control_times` is real `(N,)`, `completion_times` and `observation_times` are real `(M,)`, and `latents` is real `(M, L)`. Bounds are `0 <= N, M <= 4096`, `1 <= L <= 32`. Times lie in `[0, 1_000_000]` seconds; latent magnitudes are at most 100. Completion times increase strictly, and each observation time is at most its completion time. Observation times may be unordered because jobs can complete out of order. Control queries may also be unordered. `max_observation_age` is a scalar in `[0, 100]` seconds.

For each control time, choose the last job completed at or before it. Use that job even if its observations are older than a previous job's observations. Return a dictionary with `indices` (int64 `(N,)`, selected job or -1), `observation_age` and `completion_age` (float64 `(N,)`, control time minus the respective timestamp, NaN if absent), `usable` (Boolean `(N,)`, a job exists and observation age is at most the limit), and `context` (float64 `(N, L)`, selected latent if usable, otherwise zero).

This explicitly selects by latest completion and gates by observation age. Do not fall back to an earlier job, select a future completion or claim a real-time scheduling guarantee.

Unless a tighter bound is stated below, numeric array-like inputs must have real integer/floating dtype after `np.asarray`, be finite with absolute values <=1e6 and at most 1,000,000 entries. Boolean, complex, string and object numeric arrays are invalid; Boolean masks must have Boolean dtype. Integer arrays/scalars exclude booleans. All invalid inputs raise ValueError. Return new arrays, preserve inputs, and compute floating outputs in float64 on CPU. No automatic differentiation is required.

## Physical context and scope

Normalized observations, extrinsics, actions and latents are dimensionless. Timestamps and ages use seconds. Synchronized fixed-period state/action history; episode and completion boundaries explicit. No implicit frame or clock conversion. Original bounded adaptation teaching component. Frozen encoder and temporal alternatives do not reproduce the complete trained RMA networks or hardware benchmark.

## Example 1

Control time 1, completion time 0.9, observation time 0.5, latent [2] and maximum age 0.4 produce index 0, observation age 0.5, completion age approximately 0.1, usable false and zero context.

## Example 2

At control time 1, a job completed at 1 from observations at 1 is usable with maximum age 0; its latent [2] is returned. Future jobs remain unavailable.
