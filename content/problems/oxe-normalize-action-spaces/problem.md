# Normalize and Mask Embodiment-Specific Action Spaces

A shared model can reserve channels that some robots do not possess. Normalize observed channels using embodiment-specific statistics and separately report which entries are real supervision.

## Contract

`normalize_action_spaces(actions,available,mean,std)` receives real actions(B,H,D),1<=B<=32,1<=H<=256,1<=D<=64; available:bool(B,D); mean,std:real(B,D), std>=1e-6. Return (normalized:float64(B,H,D), mask:bool(B,H,D)), with normalized=(actions-mean)/std where available and exact0 otherwise; mask broadcasts available across horizon using fresh storage. Validate all entries including unavailable channels. Inputs already share channel ordering; no clipping or action padding is inferred.

Unless a tighter bound is stated below, numeric array-like inputs must have real integer/floating dtype after `np.asarray`, be finite with absolute values <=1e6 and at most1,000,000 entries. Boolean, complex, string and object numeric arrays are invalid; Boolean masks must have Boolean dtype. Integer arrays/scalars exclude booleans. All invalid inputs raise ValueError. Return new arrays, preserve inputs, and compute floating outputs in float64 on CPU. No automatic differentiation is required.

## Physical context and scope

Each action channel retains its declared controller unit in inputs; per-channel mean/std use that unit, output is dimensionless. H is an equally spaced action horizon supplied by the dataset; normalization does not change timing or controller frames. Original normalization/masking component inspired by OXE cross-embodiment learning. Missing dimensions are masked, not treated as observed zero commands.


## Example 1

actions=[[[3,9],[5,8]]], available=[[True,False]], mean=[[1,0]], std=[[2,1]] returns normalized=[[[1,0],[2,0]]] and mask=[[[True,False],[True,False]]].

## Example 2

actions=[[[2]],[[2]]], both available, mean=[[0],[2]], std=[[2],[1]] returns normalized=[[[1]],[[0]]]. Equal raw actions need not have equal normalized coordinates across embodiments.
