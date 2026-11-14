# Build a Heterogeneous Real, Video, and Synthetic Batch

## Intuition

A real robot demonstration supplies actuator targets, whereas an unlabelled human video does not. Batch their observations together while preserving source identity and marking only supported robot action entries as supervised.

## Mathematical mechanism

For robot row b with horizon $H_b$ and supported channels $D_b$, $$M_{bhd}=\mathbf1[source_b\ne video]\mathbf1[h<H_b]\mathbf1[d<D_b],\quad Y_{bhd}=\begin{cases}A_{bhd},&M_{bhd},\\0,&\text{otherwise}.\end{cases}$$ E is observation-feature width. A zero action can be real and supported, so masks derive from source/schema shapes rather than values. Human video uses a distinct representation, not a guessed robot control target.

## Visual computation trace

| Row source | Supplied actions | Padded action | Mask |
|---|---|---|---|
| robot | [[0],[2]] | [[0],[2]] | true,true |
| video | None | [[0],[0]] | false,false |

The table is the static visual and its text alternative; each row describes a transformation or decision.

## Worked calculation

observations=[[1],[2]],actions=[[[0],[2]],None],sources=[0,1],embodiments=[3,-1] gives actions=[[[0],[2]],[[0],[0]]], masks=[[[True],[True]],[[False],[False]]].

## Why this matters on a robot

Aggregating incompatible robot channels or source types can hide a failing embodiment. Keep provenance, masks and per-slice results visible throughout training and evaluation.

## Physical contract and limits

Normalized sensor features/actions are dimensionless; embodiment IDs are schema indices, not physical coordinates. Observations are synchronized by the caller; flow time is dimensionless and differs from physical sampling time. Original bounded interface/diagnostic inspired by GR00T N1, not a full model reproduction or real-hardware safety certification.

Source: [primary paper](https://arxiv.org/abs/2503.14734). Prerequisite: understand the observation/action schema supplied in the contract; no additional lesson is required.

## Deliberate training-scope difference

GR00T N1 uses learned latent-action targets extracted from human video and treats that representation as a separate embodiment. This exercise only collates direct robot actuator labels, so video rows have no action supervision here. A latent-action objective and its learned inverse-dynamics representation are out of scope; video rows are not claimed to be unused by the full paper.
