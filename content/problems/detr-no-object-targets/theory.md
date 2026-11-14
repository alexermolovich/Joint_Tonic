# Separate unused predictions from padded annotations

## Intuition

A detector emits a fixed number of object queries, while images contain varying numbers of annotated objects. An unmatched prediction must learn no-object. A padded annotation slot is different: it never represents a real target and must not be matched at all.

## Construct supervision after assignment

Let $Y\in\{0,\ldots,C-1\}^{B\times M}$ hold padded labels, $V\in\{0,1\}^{B\times M}$ identify real slots, and $J\in\{-1,0,\ldots,M-1\}^{B\times Q}$ hold a supplied one-to-one matching. For image b and query q,

$$
T_{bq}=
\begin{cases}
C,&J_{bq}=-1,\\
Y_{b,J_{bq}},&J_{bq}\ge0,
\end{cases}
\qquad
W_{bq}=
\begin{cases}
\lambda_{\varnothing},&J_{bq}=-1,\\
1,&J_{bq}\ge0.
\end{cases}
$$

The no-object class is the extra index C. The scalar $\lambda_{\varnothing}\in[0,1]$ downweights unused queries. This function returns target classes and per-query weights; the later loss decides its reduction.

## Visual: trace annotation indices to queries

| Query | Matched target slot | Target label | Output class | Weight |
|---|---:|---:|---:|---:|
| 0 | 1 | 0 | 0 | 1 |
| 1 | −1 | None | 2, no-object | 0.2 |
| 2 | 0 | 1 | 1 | 1 |

This trace uses C=2 and both annotation slots valid. It is a static diagram and text alternative. Reordering annotations requires updating the match indices, not rearranging queries blindly.

## Validate assignment and padding

A nonnegative match must reference a true validity slot. Matching the same target twice violates one-to-one supervision and is rejected. The API permits an incomplete valid-target matching so it can be used to inspect intermediate assignments; it does not claim every such input is the full DETR optimum.

Image-feature padding is a separate mask used inside attention. Confusing it with annotation validity can suppress real pixels or supervise nonexistent objects. This exercise handles only target-set padding.

## Why this matters on a robot

Scenes with few objects have many unused queries. Incorrect background weighting can dominate the classifier loss, while padded labels treated as objects invent phantom detections. Log assignment counts and valid-target counts when debugging training failures.

## Questions and source

Is a padded slot a background object? No, it is absent data. Why is class C reserved? Real categories occupy 0 through C−1.

Source: [DETR matching and set loss](https://arxiv.org/abs/2005.12872). First inspect [matching costs](/problems/detr-matching-cost). No training loss, Hungarian solver, or attention mask is implemented here.
