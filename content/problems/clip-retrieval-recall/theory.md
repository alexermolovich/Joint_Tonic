# Measure whether the paired observation is retrieved

## Intuition

A similarity matrix is useful only if its ranking puts the correct caption near the top. Recall at K asks a discrete question for each query: did the paired item appear among the K highest-ranked candidates? It ignores how far apart the scores are.

## Two retrieval directions

Let $S\in\mathbb R^{N\times N}$ contain dimensionless image–text scores, with row i paired to column i. Define $\pi_i$ as candidate text indices sorted by decreasing $S_{ij}$; equal scores use smaller j first. The image-to-text metric is

$$
R_{\mathrm{I\to T}}@K=\frac1N\sum_{i=0}^{N-1}
\mathbf1\{i\in\pi_i[0:K]\}.
$$

For text-to-image retrieval, sort column j over image index i and test whether j is selected. Both output scalars lie in [0,1]; they need not be equal. K is a count of candidates, not a score threshold.

## Visual: direction changes the winners

| Query direction | Query | Candidate scores | Winner at K=1 | Paired hit? |
|---|---:|---|---:|---|
| Image→text | image0 | [0.9,0.8] | text0 | Yes |
| Image→text | image1 | [0.95,0.1] | text0 | No |
| Text→image | text0 | [0.9,0.95] | image1 | No |
| Text→image | text1 | [0.8,0.1] | image0 | No |

Thus the recalls are 1/2 and 0. This table is a static trace of the exact ranking, and supplies the accessible alternative to a matrix heatmap.

## Ties and pairing

With three identical scores, candidate order is 0,1,2. At K=2 only queries0 and1 contain their diagonal positive, giving 2/3. A different arbitrary tie order could change a small benchmark, so the evaluator specifies one.

A simultaneous permutation of images and their paired texts preserves recall when scores are distinct. Permuting only one axis destroys diagonal correspondence and changes the task. Real datasets with multiple valid captions require a positive-set metric; this function deliberately assumes one positive.

## Why this matters on a robot

A robot may retrieve task descriptions or past observations to choose a skill. Global image–text retrieval does not prove object localization, safe control, or calibrated uncertainty. Report directional metrics and scene slices; a single mean can hide a camera-domain failure.

## Questions

Why can recall improve when K increases without changing the encoder? More candidates are accepted. Why is softmax unnecessary? A strictly monotonic transform preserves within-query order.

Source: [CLIP](https://arxiv.org/abs/2103.00020). Build similarities from [normalized embeddings](/problems/clip-normalize-embeddings). This is an original bounded retrieval evaluator, not the paper's full benchmark protocol.
