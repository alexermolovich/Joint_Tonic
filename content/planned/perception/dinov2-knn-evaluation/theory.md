# Inspect a representation without training another network

## Intuition

A frozen encoder is useful if nearby feature vectors share meaningful labels. A weighted nearest-neighbor classifier probes that structure without fitting a new head. Its quality still depends on the reference collection and labels.

## Similarity, neighborhood, vote

Let training rows $t_j\in\mathbb R^D$ and query rows $q_i\in\mathbb R^D$ have unit norm. Their cosine similarity is $s_{ij}=q_i^\top t_j$. For each query choose a K-element neighborhood $\mathcal N_i$ by descending similarity, breaking ties with lower training index.

With positive temperature $\tau$, define

$$
a_{ij}=\frac{\exp(s_{ij}/\tau-m_i)}
{\sum_{\ell\in\mathcal N_i}\exp(s_{i\ell}/\tau-m_i)},
\qquad
v_{ic}=\sum_{j\in\mathcal N_i}a_{ij}\mathbf1\{y_j=c\},
$$

where $m_i=\max_{j\in\mathcal N_i}s_{ij}/\tau$ and $y_j$ is the integer training label. Prediction is the class with greatest $v_{ic}$; the lower class index resolves a tie.

## Visual: one weighted neighborhood

| Neighbor | Feature | Similarity to [1,0] | Label | Normalized weight |
|---|---|---:|---:|---:|
| 0 | [1,0] | 1 | 0 | 0.7310586 |
| 1 | [0,1] | 0 | 1 | 0.2689414 |

At K=2 and temperature1, these weights are also the two class scores. This static neighborhood table is the text alternative. Multiple neighbors with the same label contribute to the same class sum.

## What is being evaluated

No encoder weights or classifier parameters change. Normalized votes sum to one, but they are not automatically calibrated probabilities. The reference implementation uses normalized votes for a clear output contract; multiplying all votes for one query by the same positive value would preserve its class ranking.

If query rows appear in the training set, a self-neighbor can inflate apparent quality. This API does not infer identity; construct disjoint evaluation splits upstream.

## Why this matters on a robot

A camera-domain shift can move otherwise similar scenes apart in feature space. Compare neighbors across lighting, camera hardware, and robot viewpoints. A strong aggregate score does not establish collision avoidance or reliable segmentation.

## Questions and source

Does a smaller temperature change which neighbors are selected? No, it changes their weights. Can an absent class win? Its vote is zero; with a nonempty neighborhood at least one observed class has positive mass.

Sources: [DINOv2](https://arxiv.org/abs/2304.07193) and its [official k-NN evaluator](https://github.com/facebookresearch/dinov2/blob/main/dinov2/eval/knn.py). This bounded CPU component omits distributed feature extraction and benchmark orchestration.
