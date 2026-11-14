# Normalize Heterogeneous Robot Observation Schemas

Robot datasets often describe the same signal under different keys and units. Normalize names and scales explicitly while refusing to guess missing channels or coordinate transforms from array shape.

## Contract

`normalize_observations(raw,mapping,scales,timestamps)` takes raw:dict of1..16 named real matrices(T,Df),1<=T<=4096,1<=Df<=64; timestamps(T,) strictly increasing seconds>=0; mapping:dict of1..16 canonical_name->existing raw_name; scales:dict with exactly mapping keys and positive numeric scalar factors<=1000. Every raw field, including unused fields, must share T and be valid. All names are ASCII identifiers matching [A-Za-z][A-Za-z0-9_]{0,31}. Return dict timestamps:float64(T,) and features:dict with exactly canonical names, each value = raw[source]*scale as an independent float64(T,Df) copy. Multiple canonical names may reference one source. Unknown source names and missing/extra scales are invalid. No implicit frame transform, resampling, offsets or missing-value fill.

Unless a tighter bound is stated below, numeric array-like inputs must have real integer/floating dtype after `np.asarray`, be finite with absolute values <=1e6 and at most1,000,000 entries. Boolean, complex, string and object numeric arrays are invalid; Boolean masks must have Boolean dtype. Integer arrays/scalars exclude booleans. All invalid inputs raise ValueError. Return new arrays, preserve inputs, and compute floating outputs in float64 on CPU. No automatic differentiation is required.

## Physical context and scope

Caller supplies multiplicative conversion factors such as centimeters to meters0.01 or degrees to radianspi/180; output units are the declared canonical units. One synchronized strictly increasing timestamp vector applies to every field; this function cannot align unsynchronized records. Original shared-schema adapter motivated by Open X-Embodiment dataset standardization. Field mapping and scaling are explicit educational policy, not the complete OXE dataset transforms.


## Example 1

raw={"p_cm":[[100],[200]]}, mapping={"position":"p_cm"}, scales={"position":0.01}, timestamps=[0,1] returns features={"position":[[1],[2]]} and timestamps=[0,1].

## Example 2

raw={"q":[[180]]}, mapping={"joint":"q","copy":"q"}, scales={"joint":pi/180,"copy":1}, timestamps=[2] returns joint=[[pi]] and copy=[[180]], with independent storage.
