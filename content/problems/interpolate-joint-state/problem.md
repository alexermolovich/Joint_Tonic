# Interpolate Joint State at Camera Time

Implement **interpolate_joint_state(times, q, queries, max_gap)**.

Accept real integer/floating array-like inputs; convert computations to float64. Require finite strictly increasing times (T,), T>=2; finite joint positions q (T,D), D>=1; finite queries (M,); and a finite positive real scalar max_gap. All input magnitudes are <=1e6. Reject bool, complex, string or object arrays and booleans for max_gap with ValueError.

Times are measurement timestamps in seconds on one synchronized clock. Joint angles are radians, already unwrapped. Queries need not be sorted. Return new float64 aligned (M,D) and bool valid (M,). An exact source timestamp is valid regardless of nearby gaps. Otherwise interpolate only inside a bracket whose duration is <=max_gap. Out-of-range or excessive-gap queries get an all-NaN row and false. Empty queries return shapes (0,D) and (0,). Preserve input values and allocate independent output arrays.

No extrapolation, nearest-neighbor substitution, angle wrapping, or clock correction. Every documented contract violation raises ValueError.

NumPy CPU; numerical tolerance rtol=1e-7, atol=1e-9. Masks, shapes and errors are exact.

## Worked examples

### Camera between encoder samples

Input: times=[0,1,2], q=[[0,2],[1,4],[2,6]], queries=[0.25,1.5], max_gap=1.

Return aligned=[[0.25,2.5],[1.5,5]] and valid=[True,True]. Each joint uses the same time fraction but its own change in angle.

### An exact sample survives a dropout

Input: times=[0,2,5], q=[[0],[2],[8]], queries=[2,3,6], max_gap=2.

Return aligned=[[2],[NaN],[NaN]] and valid=[True,False,False]. The observation at 2 s exists; 3 s lies in a 3 s gap, and 6 s needs extrapolation.

## Hints

1. Locate the first source time at or after each query with searchsorted.

2. Handle exact equality before selecting a bracket.

3. Initialize output with NaN; fill only exact or admissible rows.
