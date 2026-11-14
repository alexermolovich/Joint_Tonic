# Assemble Observation and Task Token Groups

A policy sees several token groups, such as a language goal, a camera and a state sensor. Concatenation must retain each group boundary and its presence mask; otherwise a missing sensor is indistinguishable from a real zero-valued observation.

## Contract

Inputs groups and present are Python lists of equal length G,1<=G<=16. Each group is real(B,Ng,E), common1<=B<=16,1<=E<=64,0<=Ng<=128; corresponding presence is bool(B,Ng). Total tokens L=sumNg<=512 and B*L*E<=1e6. Caller orders task groups first then observation/readout groups as desired; no implicit sorting. Return dict tokens float64(B,L,E), present bool(B,L), group_ids int64(L), offsets int64(G+1). Concatenate in list order, replace absent token features with zero, preserve present zeros. Offsets include initial0 and finalL; empty groups retain an offset entry.

Unless a tighter bound is stated below, numeric array-like inputs must have real integer/floating dtype after `np.asarray`, be finite with absolute values <=1e6 and at most1,000,000 entries. Boolean, complex, string and object numeric arrays are invalid; Boolean masks must have Boolean dtype. Integer arrays/scalars exclude booleans. All invalid inputs raise ValueError. Return new arrays, preserve inputs, and compute floating outputs in float64 on CPU. No automatic differentiation is required.

## Physical context and scope

Token features and normalized actions are dimensionless; no world-frame transform or physical actuation is performed. Each batch row is a synchronized caller-supplied policy context; group order is explicit. Original bounded interface exercise motivated by Octo modular adaptation; this is not its full transformer or diffusion policy.


## Example 1

groups=[[[[1]]],[[[2],[3]]]], present=[[[True]],[[True,False]]] gives tokens=[[[1],[2],[0]]], present=[[True,True,False]], group_ids=[0,1,1], offsets=[0,1,3].

## Example 2

Two empty groups of shape(1,0,2) return tokens(1,0,2), presence(1,0), group_ids(0), offsets=[0,0,0].
