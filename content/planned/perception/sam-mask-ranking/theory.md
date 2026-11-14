# Choose masks using the model's quality estimate

## Intuition

One prompt can reasonably describe a whole object or one of its parts. A promptable decoder may produce several candidate masks and a learned score for each. Ranking chooses interpretations; averaging their pixels would create a different, potentially meaningless region.

## Stable score ranking

Let $M\in\{0,1\}^{N\times H\times W}$ contain N candidate masks on one image grid and $s\in\mathbb R^N$ their dimensionless predicted-quality scores. Define a permutation $\pi$ by sorting the keys $(-s_i,i)$ in ascending order. For the requested count K,

$$
\widehat M_j=M_{\pi_j},\qquad
\widehat s_j=s_{\pi_j},\qquad 0\le j<K.
$$

The second key gives a deterministic tie rule. Return original indices as well so subsequent depth or instance metadata can follow the same choices.

## Visual: geometry travels with its index

| Candidate | Binary row | Predicted score | Rank |
|---|---|---:|---:|
| 0 | [1,0] | 0.7 | 3 |
| 1 | [0,1] | 0.9 | 1 |
| 2 | [1,1] | 0.8 | 2 |

For K=2 select rows1 and2. The selected mask pixels remain unchanged. This table serves as a static diagram and text alternative.

## Predicted quality is not measured IoU

A learned IoU-quality head is a regression output. This contract accepts its raw finite score even outside [0,1]; clipping could create artificial ties and change ranking. Real measured intersection-over-union requires a ground-truth mask:

$$
\operatorname{IoU}(A,B)=\frac{|A\cap B|}{|A\cup B|}.
$$

Here A and B denote pixel sets. That quantity is not available merely because a model predicts a score. This task does not calculate ground-truth IoU or certify calibration.

## Why this matters on a robot

A high-quality-looking mask can select the wrong part or a transparent surface. Before attaching depth or computing a grasp frame, preserve the image's resizing/cropping transform and verify semantic identity separately. Ranking cannot fix a stale cached image embedding or incorrectly mapped prompt.

Empty selections retain H and W, allowing downstream pipelines to distinguish no detections from a changed image resolution. Duplicate or overlapping masks are retained; suppression is a separate policy.

## Questions and source

Why return original indices? To align all candidate metadata. Why not remove overlapping masks here? Ranking and duplicate suppression answer different questions and have different thresholds.

Source: [SAM](https://arxiv.org/abs/2304.02643) and its [official mask decoder](https://github.com/facebookresearch/segment-anything/blob/main/segment_anything/modeling/mask_decoder.py). This task isolates candidate selection, not the encoder, prompts, or quality-head training.
