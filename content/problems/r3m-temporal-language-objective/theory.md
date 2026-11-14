# Combine Temporal and Language Alignment Losses

## Intuition

Nearby visual states, meaningful language progress and compact features provide different learning signals. Compute each term explicitly before combining them, so a large regularizer cannot hide a reversed contrastive target.

## Mathematical mechanism

For row $b$, supplied embeddings $z_i,z_j,z_k,z_o\in\mathbb R^D$ have dimensionless coordinates. Define three temporal scores $$s_b=[-\|z_i-z_j\|_2,-\|z_i-z_k\|_2,-\|z_i-z_o\|_2],\quad \ell_t=\operatorname{LSE}(s_b)-s_{b0}.$$ Here $\operatorname{LSE}(x)=m+\log\sum_c e^{x_c-m}$ with $m=\max_c x_c$. Supplied language logits $g_b\in\mathbb R^3$ order later-correct progress first, then earlier progress and unrelated-video progress. Their loss is $$\ell_l=\operatorname{LSE}(g_b)-g_{b0},\quad \ell_1=\sum_d|z_{id}|,\quad \ell_2=\sqrt{\sum_d z_{id}^2}.$$ L2 is a norm, not its square. With valid mask $M_b$ and weights $w\in\mathbb R^4$, $$c=\frac{\sum_b M_b[\ell_t,\ell_l,\ell_1,\ell_2]}{\sum_b M_b},\qquad L=w^\top c.$$ Set all terms to zero if no row is valid. This pins a valid-row mean and one anchor representation per row; the paper also combines temporal, language, L1 and L2 terms, with its own batch reduction and weights.

## Visual computation trace

| Anchor [3,4], all compared embeddings identical | Component |
|---|---|
| Three equal temporal scores | log(3) |
| Three equal language logits | log(3) |
| Absolute-coordinate sum | 7 |
| Euclidean norm | 5 |
| Weights [0,0,2,3] | 29 |

The table is the static visual and its text alternative; each row describes a transformation or decision.

## Worked calculation

B=D=1, all four embeddings zero, language logits [0,0,0], valid True, weights [1,1,1,1]: components [log(3),log(3),0,0], loss 2log(3).

## Why this matters on a robot

Using squared distance changes temporal score geometry; using squared L2 changes regularization strength. Treating the language term as caption matching also misses its progress ordering. A low toy loss does not prove useful manipulation features.

## Physical contract and limits

Embedding coordinates, supplied logits, normalized robot state and normalized actions are dimensionless. Frame indices are ordinal positions, not timestamps in seconds. Triplets stay in one video and the negative comes from another. Policy rows are supplied observations with explicit training/evaluation membership; no temporal transitions are inferred. Original bounded R3M component. The sampler is an explicit sequential recorded-draw recipe, the loss pins valid-row mean reduction and anchor regularization, and the policy uses an affine head rather than the paper's BatchNorm/MLP. No pretrained model or benchmark reproduction claim.

Source: [primary paper](https://arxiv.org/html/2203.12601v3). Prerequisite: understand the observation/action schema supplied in the contract; no additional lesson is required.
