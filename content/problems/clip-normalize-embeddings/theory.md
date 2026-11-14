# Theory

## Intuition: compare direction rather than raw feature length

An image encoder and a text encoder produce vectors in a learned shared feature space. Their coordinate magnitudes can differ even when the semantic direction is similar. Row normalization removes that scale before a dot product compares directions. It does not make a poor encoder semantically correct or turn similarity into a calibrated probability.

This exercise prepares the representations. The existing [symmetric CLIP loss](/problems/clip-symmetric-loss) continues with a full pairwise score matrix and two retrieval objectives. Complete this normalization component first; it does not replace that loss problem.

## Define the normalization

Let $V,T\in\mathbb R^{B\times D}$ contain paired image and text embeddings. $B$ counts paired samples, $D$ is embedding width, and $v_i,t_i\in\mathbb R^D$ are individual rows. Components and norms have no physical units. Each row is nonzero under the contract.

$$
r_i=\|v_i\|_2=\sqrt{\sum_{d=1}^{D}v_{id}^2},\qquad
\bar v_i=v_i/r_i,\qquad
\bar t_i=t_i/\|t_i\|_2.
$$

Norms have shape $(B,1)$ when retained for broadcasting. Summing over the batch axis instead would normalize each feature across different images, coupling unrelated robot observations.

For a later comparison, $\bar v_i^\top\bar t_j$ equals cosine similarity and lies in $[-1,1]$ up to floating-point error. Temperature scaling and softmax are later operations; unit normalization alone does not produce a probability distribution.

## Worked numerical and gradient example

For $v=[3,4]$, $r=5$ and $\bar v=[0.6,0.8]$. Compared with normalized text $[0,1]$, the dot product is $0.8$. Rescaling $v$ to $[30,40]$ leaves this result unchanged. A zero vector has no defined direction, so it is rejected rather than silently turned into a unit vector.

The local derivative with respect to an unconstrained input row is

$$
\frac{\partial\bar v}{\partial v}=
\frac{1}{r}\left(I_D-\bar v\bar v^\top\right),
$$

where $I_D$ is the $D\times D$ identity. For $v=[3,4]$, the derivative of the first normalized component is $[0.128,-0.096]$. This explains why detaching the result would break encoder training even though its forward values look right. No custom backward function is required; ordinary PyTorch operations preserve it.

## Visual: keep the sample axis intact

| Stream | Input rows | Norm per row | Output rows |
|---|---|---|---|
| Images | [3,4]; [0,−2] | 5; 2 | [0.6,0.8]; [0,−1] |
| Texts | [0,5]; [−8,6] | 5; 10 | [0,1]; [−0.8,0.6] |

Each row keeps its sample identity. The B×1 norm broadcasts over D feature coordinates; images and texts never share a denominator.

Text alternative: normalize each modality separately along its last axis. Row zero remains row zero in both outputs; no sorting or cross-modal mixing occurs. Example 1's image lengths `[5,2]` and text lengths `[5,10]` each become `[1,1]`.

## Why this matters on a robot

An unexpectedly zero feature may indicate a failed preprocessing or model export path. Rejecting it makes that failure visible. A wrong normalization axis can make a frame's prediction depend on unrelated frames in the batch. Store preprocessing versions and monitor norm distributions, but evaluate spatial grounding separately from global image/text similarity.

Source: [CLIP section 2.3 and Figure 3](https://arxiv.org/abs/2103.00020). The bounded CPU exercise excludes encoders, tokenization, prompt ensembling, and training. Its theory and examples are original.

## Check your understanding

1. Can normalizing across the batch dimension make one observation depend on other observations?
2. Why can a numerically correct detached output still fail this task?

Discuss these after working through the numerical example. Answers are in [examples.md](#).
