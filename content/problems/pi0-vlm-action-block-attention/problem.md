# Build Block Attention for VLM and Action Expert Tokens

The semantic context remains fixed while an action chunk is jointly refined. Context tokens can read each other, action tokens can read that context and the other actions, but context must not depend on the changing action tokens.

## Contract

context_present bool(B,C), action_present bool(B,A),common1<=B<=16,0<=C<=128,1<=A<=128. Return bool(B,C+A,C+A) in context-then-action order. Present context queries read all present context keys and NO action keys. Present action queries read all present context AND action keys, bidirectionally within the action chunk. Absent query/key positions are entirely disabled. No tokenwise causal triangle; this is a two-block conditioning mask, not a full released model mask with separately encoded state/time groups.

Unless a tighter bound is stated below, numeric array-like inputs must have real integer/floating dtype after `np.asarray`, be finite with absolute values <=1e6 and at most1,000,000 entries. Boolean, complex, string and object numeric arrays are invalid; Boolean masks must have Boolean dtype. Integer arrays/scalars exclude booleans. All invalid inputs raise ValueError. Return new arrays, preserve inputs, and compute floating outputs in float64 on CPU. No automatic differentiation is required.

## Physical context and scope

Normalized actions and token features are dimensionless; physical calibration is supplied upstream. Caller-synchronized observations; generation time and physical control time are distinct. Original bounded engineering component motivated by the paper; no pretrained model or benchmark reproduction is implied.


## Example 1

context=[[True]], action=[[True,True]] gives mask[[[1,0,0],[1,1,1],[1,1,1]]] as booleans.

## Example 2

context=[[False]], action=[[True,False]] gives only mask[0,1,1]=True; all other entriesFalse.
