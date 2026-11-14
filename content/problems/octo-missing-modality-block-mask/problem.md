# Build Block Masks for Missing Sensors and Goals

Attention visibility is a directed permission rule. An observation may read a goal without granting the goal access to every observation, and an absent token must be disabled as both a query and a key.

## Contract

group_ids integer(L,),0<=L<=256; group_rules bool(G,G),1<=G<=16; present bool(B,L),1<=B<=16. IDs in0..G-1. Return bool(B,L,L): query i may read key j when group_rules[group_ids[i],group_ids[j]] and both positions are present. Rules are directed query-group by key-group. There is no extra temporal triangle or forced diagonal; callers encode their policy in group_rules. Entirely false query rows are permitted and must be skipped by a downstream attention operator.

Unless a tighter bound is stated below, numeric array-like inputs must have real integer/floating dtype after `np.asarray`, be finite with absolute values <=1e6 and at most1,000,000 entries. Boolean, complex, string and object numeric arrays are invalid; Boolean masks must have Boolean dtype. Integer arrays/scalars exclude booleans. All invalid inputs raise ValueError. Return new arrays, preserve inputs, and compute floating outputs in float64 on CPU. No automatic differentiation is required.

## Physical context and scope

Token features and normalized actions are dimensionless; no world-frame transform or physical actuation is performed. Each batch row is a synchronized caller-supplied policy context; group order is explicit. Original bounded interface exercise motivated by Octo modular adaptation; this is not its full transformer or diffusion policy.


## Example 1

IDs=[0,1], rules=[[True,False],[True,True]], present=[[True,True]] gives [[[True,False],[True,True]]].

## Example 2

With the same IDs/rules and present=[[False,True]], output is [[[False,False],[False,True]]].
