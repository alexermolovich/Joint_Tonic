# Select Geometric Pose Inliers

## Intuition

Image-feature agreement should be tested against geometry, with uncertainty determining how much a given pixel discrepancy matters. Comparing supplied hypotheses makes the scoring logic visible separately from pose estimation.

## Mathematics and conventions

For pose k, transform world landmark $P_i$ into camera coordinates and project to $\hat u_{ki}$. With measured pixel $u_i$ and isotropic pixel standard deviation $\sigma_i$, define

$$e_{ki}^2=\frac{\|\hat u_{ki}-u_i\|_2^2}{\sigma_i^2},\qquad I_{ki}=\mathbf1\{e_{ki}^2\le\eta\}.$$

Only valid observations with camera depth above $10^{-6}$ m are supported. Errors and eta are dimensionless; sigma has pixel units. Count inliers per hypothesis and take the median only over those inliers. The ordering $(-count,median,index)$ makes evidence quantity primary and residual quality a tie breaker. Behind-camera points cannot become inliers even at a permissive threshold.

## Visual computation trace

| Hypothesis | Projected x | Measured x | Normalized squared error |
| --- | --- | --- | --- |
| Identity | 0 | 1 | 1 |
| Camera translation +1x | 1 | 1 | 0 |
| Equal inlier counts | | | second hypothesis wins |

## Worked examples

1. World point `[[0.,0.,1.]]`, observed pixel `[[1.,0.]]`, identity pose, intrinsics `[1.,1.,0.,0.]`, std 1 and threshold 1: normalized squared error 1 and one inlier.
2. Add a second pose with camera-from-world x translation +1 m. Its projected pixel is `[1.,0.]`, giving zero error. Both hypotheses have one inlier, so the second pose wins on median error.

## Why this matters on a robot

A hypothesis may explain many points on a moving object, and overestimated pixel uncertainty can make poor geometry appear acceptable. These scores require appropriate input correspondences and cannot replace robust pose estimation.

## Source and prerequisites

[Primary paper](https://arxiv.org/abs/1610.06475). [project-camera-points](/problems/project-camera-points)

This static explanation has no animation; its tables and shape traces are the text equivalent of the computation.
