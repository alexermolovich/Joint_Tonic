# Filter Automatic Masks by Stability and Overlap

## Intuition

A strong quality score does not tell us whether a tiny threshold change erases the mask. First test threshold stability, then remove redundant candidates. These checks measure different things: stability concerns one candidate; overlap compares two candidates.

## Threshold stability

For candidate $i$ and pixel $p$, let $z_{ip}$ be a dimensionless mask logit. With base threshold $\theta$ and positive perturbation $\delta$, define

$$
B_i=\{p:z_{ip}>\theta\},\quad
H_i=\{p:z_{ip}>\theta+\delta\},\quad
L_i=\{p:z_{ip}>\theta-\delta\}.
$$

Because $\delta>0$, $H_i\subseteq B_i\subseteq L_i$. Therefore the IoU of the high and low masks simplifies to

$$
s_i=\begin{cases}|H_i|/|L_i|,&|L_i|>0,\\0,&|L_i|=0.\end{cases}
$$

Areas count pixels on one common image grid. Eligibility requires a nonempty base mask and $s_i\ge s_{\min}$, where $s_{\min}$ is the supplied stability threshold. The explicit empty policy prevents an all-background candidate from becoming a useful object merely because both perturbed masks agree.

## Visual: filter, order, compare

| Candidate | Base pixels | High/low counts | Stability | Quality | Outcome |
|---|---|---|---:|---:|---|
| 0 | first two | 2 / 2 | 1 | 0.6 | suppressed by 1 |
| 1 | first two | 2 / 2 | 1 | 0.9 | kept |
| 2 | first two | 1 / 2 | 0.5 | 1.0 | fails stability |

This original table is a static pipeline and text alternative for example 1. Ranking before eligibility would let candidate 2 incorrectly suppress a stable candidate.

## Greedy overlap filtering

For two nonempty base masks, use

$$
\operatorname{IoU}(B_i,B_j)=
\frac{|B_i\cap B_j|}{|B_i\cup B_j|}.
$$

Visit candidates by descending quality $q_i$ with index as the deterministic tie-break. Suppress $i$ if any previously kept $j$ has IoU strictly above the supplied overlap threshold $\eta$. Compare against kept masks only: a previously suppressed mask cannot suppress another candidate. In example 2, the areas are 1 and 2, intersection 1, and IoU 0.5; equality with $\eta=0.5$ passes.

This mask-overlap variant is deliberately different from SAM's box-based NMS. Two disjoint thin masks can have strongly overlapping boxes; the two filters need not agree.

## Why this matters on a robot

Repeated masks can duplicate grasp candidates or object counts. A stable mask can nevertheless cover the wrong object, and a visually correct mask does not identify safe contact surfaces. Transform masks into the appropriate original image coordinates before associating calibrated depth. Here the shared input grid is already aligned.

## Sources and prerequisites

[Segment Anything](https://arxiv.org/abs/2304.02643) and its [stability utility](https://github.com/facebookresearch/segment-anything/blob/main/segment_anything/utils/amg.py) motivate the threshold test. The empty policy, bounded API, and mask-IoU suppression are original teaching choices. Prerequisite: [rank candidate masks](/problems/sam-mask-ranking).

