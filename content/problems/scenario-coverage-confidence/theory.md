# Estimate Scenario Coverage and Confidence Intervals

## Intuition

A perfect observed success rate from one trial is weak evidence. Keep missing scenario coverage separate from uncertainty within measured buckets.

## Count, then quantify uncertainty

For bucket b, let n_b be its trial count and k_b its successful-trial count, both dimensionless integers. The rate is p_b=k_b/n_b only when n_b>0. With fixed normal score z=1.96, the Wilson center and half-width are

$$c_b=\frac{p_b+z^2/(2n_b)}{1+z^2/n_b},\qquad h_b=\frac{z\sqrt{p_b(1-p_b)/n_b+z^2/(4n_b^2)}}{1+z^2/n_b}.$$

Return [c_b-h_b,c_b+h_b] clipped to[0,1]. Coverage C counts observed buckets, not successful trials:

$$C=\frac{1}{B}\sum_{b=0}^{B-1}\mathbf1[n_b>0].$$

B is the declared scenario-bucket count. This normal-score interval is an original evaluation extension; the domain-randomization paper does not prescribe this gate.

## Visual evidence trace and worked example

| Bucket | Successes/trials | Rate | Wilson interval |
|---|---|---|---|
| 0 | 1/1 | 1 | approximately[0.20654,1] |
| 1 | 0/0 | unknown | unknown |

Coverage is1/2. This static table also supplies the text alternative.

## Why this matters on a robot

Repeated frames from one rollout are correlated and must not be treated as independent trials. A large number of nominal-camera successes also cannot fill an untested lighting bucket. Report unknown evidence instead of replacing it with zero-width intervals.

Prerequisite: [Measure Performance Across Shift Buckets](/problems/shift-bucket-performance).

## Source and scope

This original bounded component is motivated by [2017-domain-randomization](https://arxiv.org/abs/1703.06907). It does not reproduce the full paper, trained model or benchmark protocol.
