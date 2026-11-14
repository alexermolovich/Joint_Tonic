# Give each point its cloud's global context

## Intuition

A point's local feature may describe an edge without telling whether that edge belongs to a handle or a leg. A pooled cloud feature gives context. Concatenating both lets a later per-point classifier combine local evidence with object-level information.

## Shape and index rule

Let $L\in\mathbb R^{B\times N\times D}$ hold B clouds, N point slots and D local feature channels. Let $G\in\mathbb R^{B\times E}$ hold E global channels per cloud. These learned coordinates have no physical length units. The fused feature is

$$
F_{b,n,:}=[L_{b,n,:};G_{b,:}]
\in\mathbb R^{D+E},\qquad
F\in\mathbb R^{B\times N\times(D+E)}.
$$

The semicolon denotes concatenation along the feature axis. This is not addition: D and E can differ. Broadcasting G over N repeats the same context for every point in a cloud, never across unrelated batch elements.

## Visual: two points share context

| Point | Local feature | Global context | Fused feature |
|---|---|---|---|
| 0 | [1,2] | [10,20,30] | [1,2,10,20,30] |
| 1 | [3,4] | [10,20,30] | [3,4,10,20,30] |

Read left to right to trace channel order. The output shape is (1,2,5). This static table is the text alternative.

## Invariance versus equivariance

If the global descriptor was produced by a symmetric pool, reordering points leaves it unchanged. The fused rows then reorder in exactly the same way as the local rows:

$$
F(\Pi L,G)=\Pi F(L,G).
$$

Here $\Pi$ permutes the N point positions independently within a cloud. This property is permutation **equivariance**. Segmentation predictions must follow the points; a fully invariant per-point output would lose correspondence.

## Why this matters on a robot

Scene segmentation can use global shape context to distinguish similar local surfaces. Mixing batch indices contaminates one scene with another's context. Combining features from different timestamps can similarly create an internally inconsistent grasp target even when all dimensions match.

The caller must preserve padding masks for later classifiers. This concatenation does not decide which slots are real points or zero out padding.

## Questions and source

Why can D and E differ? Concatenation joins coordinates instead of pairing them. Why does an empty point axis produce no rows? There are no per-point predictions to condition.

Source: [PointNet segmentation architecture](https://arxiv.org/abs/1612.00593). The prerequisite [symmetric pooling](/problems/pointnet-symmetric-pooling) constructs one possible global feature. This task implements only the local/global interface.
