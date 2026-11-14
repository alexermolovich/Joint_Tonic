# Report Metrics by Source and Embodiment

A high average success rate can hide a weak source or robot embodiment. Keep a source-by-embodiment table, distinguish missing evidence from failure, and compute latency percentiles inside each cell.

## Contract

source_ids integer(N,)0realrobot,1humanvideo,2syntheticrobot; embodiment_ids integer(N,) in0..E-1, E=num_embodiments integer1..16; success bool(N,); latency_ms real(N,)nonnegative;0<=N<=10000. All rows are labelled evaluation records already assigned to a target robot embodiment; video-source evaluation uses an explicit adapted robot test, not inferred video actions. Return count int64(3,E), success_rate float64(3,E), p95_latency_ms float64(3,E); no records gives NaN for both metrics. p95 nearest rank ceil(.95*n)-1 WITHIN each cell. Also overall_success float (allNmean) or None ifempty, and worst_observed_success float(minfinite cell rate) or None. Counts include failed trials, no source reweighting.

Unless a tighter bound is stated below, numeric array-like inputs must have real integer/floating dtype after `np.asarray`, be finite with absolute values <=1e6 and at most1,000,000 entries. Boolean, complex, string and object numeric arrays are invalid; Boolean masks must have Boolean dtype. Integer arrays/scalars exclude booleans. All invalid inputs raise ValueError. Return new arrays, preserve inputs, and compute floating outputs in float64 on CPU. No automatic differentiation is required.

## Physical context and scope

Latency milliseconds; source/embodiment labels are fixed evaluation schema indices; success is binary closed-loop trial outcome. Observations are synchronized by the caller; flow time is dimensionless and differs from physical sampling time. Original bounded interface/diagnostic inspired by GR00T N1, not a full model reproduction or real-hardware safety certification.


## Example 1

sources=[0,0,2],embodiments=[0,0,1],success=[True,False,True],latency=[2,4,3],E2 gives count[[2,0],[0,0],[0,1]], populated rates .5 and1, populated p95 4 and3,overall2/3,worst.5.

## Example 2

All arrays empty with E1 returns zero count(3,1), NaN metrics and overall/worst None.
