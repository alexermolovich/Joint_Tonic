# Route Tokens into Dataset-Specific Action Heads

Two robots can share a policy representation while having different action widths. Route each readout through the correct robot head and explicitly mark which padded output channels describe real actuators.

## Contract

readouts real(B,E),1<=B<=128,1<=E<=64; dataset_ids int(B,); weights real(G,E,D),1<=G<=16,1<=D<=32; biases real(G,D); dimensions int(G,) with1<=dimensions[g]<=D. IDs0..G-1. For each row apply its dataset-specific affine head, then zero dimensions at or beyond its declared width. Return actions float64(B,D) and available bool(B,D). No activation or action denormalization; readouts already summarize observation tokens.

Unless a tighter bound is stated below, numeric array-like inputs must have real integer/floating dtype after `np.asarray`, be finite with absolute values <=1e6 and at most1,000,000 entries. Boolean, complex, string and object numeric arrays are invalid; Boolean masks must have Boolean dtype. Integer arrays/scalars exclude booleans. All invalid inputs raise ValueError. Return new arrays, preserve inputs, and compute floating outputs in float64 on CPU. No automatic differentiation is required.

## Physical context and scope

Token features and normalized actions are dimensionless; no world-frame transform or physical actuation is performed. Each batch row is a synchronized caller-supplied policy context; group order is explicit. Original bounded interface exercise motivated by Octo modular adaptation; this is not its full transformer or diffusion policy.


## Example 1

readouts=[[2],[2]], IDs=[0,1], weights=[[[1,2]],[[3,4]]], biases=[[1,1],[1,1]], dimensions=[1,2] gives actions=[[3,0],[7,9]], available=[[True,False],[True,True]].

## Example 2

readout=[[0]], ID=[0], weights=[[[5]]], bias=[[0]], dimensions=[1] gives action[[0]] with available[[True]].
