# Detect Paused or Corrupted Action Segments

## Contract

`action_segment_report(times_ns, actions, observed, max_command, deadband, min_samples, min_duration_ns) -> dict`. times_ns is NumPy int64(T,),0<=T<=100000, values0..2^63-1 strictly increasing; actions NumPy float32/float64(T, D),1<=D<=32, at most 10^6 entries; NaN/Inf and any finite magnitudes are accepted as evidence. observed bool(T,), max_command float32/float64(D,) finite in(0,1e6]. deadband is finite built-in real in 0..min(max_command), min_samples built-in int in 1..100000, min_duration_ns built-in int in 0..2^63-1. Array dtypes/shapes and scalar contracts are validated; noncontiguous arrays are valid.

A corrupt row is unobserved OR has any nonfinite action OR any abs(action)>max_command. A pause candidate is a noncorrupt row with every abs(action)<=deadband. Find maximal contiguous candidate runs[start, end) in sample-index order. Mark a run paused only if end-start>=min_samples AND times_ns[end-1]-times_ns[start]>=min_duration_ns (exact integer ns). A corrupt row splits runs. Return corrupt:bool(T,), paused:bool(T,), segments:list[(start, end, duration_ns)] for qualifying maximal runs in order; tuple values Python ints. Empty T returns empty outputs. Actions are joint velocity commands in rad/s in caller-ordered actuator axes; no actual motion, contact or safety is inferred. Work O(TD).

## Common operational contract

Identifiers are ASCII strings matching [a-z][a-z0-9_-]{0,31}; digests are exactly 64 lowercase hexadecimal characters. Unless the task explicitly reports malformed field values as issues, invalid argument types, fields, bounds, IDs or unknown references raise ValueError. Built-in integer scalars exclude bool. Preserve all input arrays/records and return fresh containers. No network, filesystem reads, wall clock, randomness or physical robot commands are used. These are original bounded operational policies inspired by the source paper, not its released API or a certification.

## Worked examples

times[0,10,20,30], actions[[0],[0],[1],[0]], all observed flags=True, max_command[2], deadband=0.1, min_samples=2, min_duration_ns=10 yields corrupt[F, F, F, F], paused[T, T, F, F], segments[(0,2,10)].

With times[0,10,20], actions[[0],[NaN],[0]], all observed flags=True, max_command[2], deadband=0.1, min_samples=2, min_duration_ns=0, corrupt[F, T, F], paused[F, F, F], segments[]. The corrupt row separates two short runs.

## Source and scope

Original bounded component inspired by [2018-roboturk](https://arxiv.org/abs/1811.02790). It does not reproduce the full paper or establish hardware safety or data-use authorization.
