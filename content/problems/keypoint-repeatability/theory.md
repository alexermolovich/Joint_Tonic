# Evaluate Keypoint Repeatability

## Intuition

A detector should find the same scene locations after a known image warp. First exclude points that cannot be observed in both images; then ask the nearest-neighbor question independently in each direction.

## Mathematics and conventions

Let A and B be the sets of eligible points in source and target image coordinates, respectively. Let $\pi_H$ be homogeneous projection by the supplied source-to-target matrix H. For $a_i\in A$,

$$c_i^A=\mathbf1\{\min_{b_j\in B}\|\pi_H(a_i)-b_j\|_2\le\tau\}.$$

For $b_j\in B$, define $c_j^B$ analogously with $H^{-1}$ and distances in source pixels. The symmetric score is

$$R=\frac{\sum_i c_i^A+\sum_j c_j^B}{|A|+|B|}.$$

Tau is a pixel tolerance in the image where each distance is measured. Under scale changes the two directional distances need not be equal. Empty opposite sets produce zero correctness; an empty denominator produces an undefined score. No assignment constraint removes duplicate detections.

## Visual computation trace

| Direction | Eligible points | Correct at threshold 0 |
| --- | --- | --- |
| Source to target | (0,0),(2,0) | first only: 1/2 |
| Target to source | (0,0) | 1/1 |
| Combined | three directional detections | 2/3 |

## Worked examples

1. Identity warp, source points `[[0.,0.],[2.,0.]]`, target `[[0.,0.]]`, both image sizes `[3,3]`, threshold 0: source correctness `[True,False]`, target correctness `[True]`, repeatability `2/3`.
2. The same image sizes with one point `[0.,0.]` in each image and target-from-source x translation +3 have no shared support. Both eligibility flags are False and repeatability is NaN.

## Why this matters on a robot

A feature detector that produces many repeated corners on one object can have good repeatability but poor pose coverage. This metric alone cannot prove that the correspondences constrain camera motion.

## Source and prerequisites

[Primary paper](https://arxiv.org/abs/1712.07629). [homographic-keypoint-adaptation](/problems/homographic-keypoint-adaptation)

This static explanation has no animation; its tables and shape traces are the text equivalent of the computation.
