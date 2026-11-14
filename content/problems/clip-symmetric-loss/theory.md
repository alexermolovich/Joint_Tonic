# Matching image and language features

## Intuition

The batch is a small matching game. Every image must identify one instruction among B candidates, and every instruction must identify one image. Similarity alone is insufficient: if every embedding points in the same direction, all candidates look equally likely.

## Tensors and mathematics

Let V and T be image and text feature matrices in R^(B×D). Normalize row vectors v_i and t_j to obtain z_i and w_j. The representations and logits are dimensionless; this operation does not convert robot coordinate frames or distances.

$$
z_i=\frac{v_i}{\lVert v_i\rVert_2},\qquad
w_j=\frac{t_j}{\lVert t_j\rVert_2},\qquad
S_{ij}=\frac{z_i^\top w_j}{\tau}.
$$

Here τ > 0 is temperature. A smaller temperature makes probability mass concentrate more sharply on high-similarity candidates.

The image-to-text loss for row i is the negative log probability assigned to its own text, indexed by i. Symmetric training also asks each text to retrieve its image.

$$
\mathcal L=\frac{1}{2B}\sum_{i=1}^{B}
\left[
-S_{ii}+\log\sum_j e^{S_{ij}}
-S_{ii}+\log\sum_j e^{S_{ji}}
\right].
$$

Use a stable cross-entropy or log-sum-exp operation. Explicit exponentiation can overflow when τ is small.

## Visual lesson

The CLIP visual shows the similarity matrix as a heatmap. Diagonal cells represent known pairs; off-diagonal cells are negatives. Changing temperature should update a selected row's probability distribution. A table of logits, target indices and row/column probabilities supplies the same information for keyboard and screen-reader users.

## Worked example

With two matching orthogonal vectors and τ=1, each row is [1,0] or [0,1]. The target probability is e/(e+1), so the loss is approximately 0.313262. When texts are swapped, the target probability falls to 1/(e+1), yielding 1.313262.

Multiplying a feature row by a positive scalar should not change the result after normalization. That is a useful diagnostic for an accidentally omitted normalization step.

## Why this matters on a robot

Language-conditioned perception often reuses a visual-language embedding space. A broken negative set or pair ordering can teach a robot the wrong object-instruction associations even when every tensor shape is valid. Batch duplication can create false negatives; a singleton batch offers no useful contrastive signal. Temperature, preprocessing versions and pair construction belong in the training manifest.

## Failure modes and scope

Normalizing over B mixes unrelated samples. Averaging only one direction changes the objective. Taking a Python float destroys gradients. High retrieval performance alone does not establish grounding, spatial reasoning or safe control.

The [CLIP paper](https://arxiv.org/abs/2103.00020) motivates this objective. Here τ is supplied directly and embeddings are given; the web-scale dataset, encoders and training pipeline are outside the exercise.
