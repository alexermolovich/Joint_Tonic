# Build a Heterogeneous Real, Video, and Synthetic Batch

A real robot demonstration supplies actuator targets, whereas an unlabelled human video does not. Batch their observations together while preserving source identity and marking only supported robot action entries as supervised.

## Contract

observations real(B,E),1<=B<=32,1<=E<=128; actions PythonlistB; source_ids integer(B,)0=realrobot,1=humanvideo,2=syntheticrobot; embodiment_ids integer(B,). Video rows must have actions=None and embodiment=-1. Real/synthetic rows require embodiment0..15 and real action matrix(Hi,Di),1<=Hi<=64,1<=Di<=32; all action rows supplied in caller-normalized embodiment channel order. Pad action dimensions/time to max Hi,Di across ROBOT rows; if no robot rows use(0,0). Return observations copy, actions float64(B,Hmax,Dmax) exact0padding, action_mask bool same shape true only supplied robot entries, source_ids/embodiment_ids int64copies. Human video may train another objective but contributes no invented actuator labels. Reject None robot actions and any numeric video actions.

Unless a tighter bound is stated below, numeric array-like inputs must have real integer/floating dtype after `np.asarray`, be finite with absolute values <=1e6 and at most1,000,000 entries. Boolean, complex, string and object numeric arrays are invalid; Boolean masks must have Boolean dtype. Integer arrays/scalars exclude booleans. All invalid inputs raise ValueError. Return new arrays, preserve inputs, and compute floating outputs in float64 on CPU. No automatic differentiation is required.

## Physical context and scope

Normalized sensor features/actions are dimensionless; embodiment IDs are schema indices, not physical coordinates. Observations are synchronized by the caller; flow time is dimensionless and differs from physical sampling time. Original bounded interface/diagnostic inspired by GR00T N1, not a full model reproduction or real-hardware safety certification.

## Deliberate training-scope difference

GR00T N1 uses learned latent-action targets extracted from human video and treats that representation as a separate embodiment. This exercise only collates direct robot actuator labels, so video rows have no action supervision here. A latent-action objective and its learned inverse-dynamics representation are out of scope; video rows are not claimed to be unused by the full paper.


## Example 1

observations=[[1],[2]],actions=[[[0],[2]],None],sources=[0,1],embodiments=[3,-1] gives actions=[[[0],[2]],[[0],[0]]], masks=[[[True],[True]],[[False],[False]]].

## Example 2

One video row observations=[[5]],actions=[None],source[1],embodiment[-1] gives actions/mask shape(1,0,0); it remains an observation example.
