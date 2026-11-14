# A shared contract between tokens and motion

## Intuition

Quantization replaces a continuum with a finite vocabulary. The model chooses a region of action space; the decoder turns that choice into one representative command. Choosing bin centers reduces the largest reconstruction error compared with choosing bin edges.

## Mathematics and units

For one dimension, let a be the action, l and u the bounds in that dimension's physical units, and B the number of bins. Let o be a reserved token offset. First clip and normalize:

$$
a_c=\min(u,\max(l,a)),\qquad r=\frac{a_c-l}{u-l}.
$$

The bin index q and token k are dimensionless integers. The reconstruction has the original physical unit.

$$
q=\min(B-1,\lfloor Br\rfloor),\qquad
k=q+o,\qquad
\hat a=l+\left(q+\frac12\right)\frac{u-l}{B}.
$$

For actions within the declared range, the maximum reconstruction error is half a bin width:

$$
|a-\hat a|\leq\frac{u-l}{2B}.
$$

For out-of-range commands this bound applies to a_c, not the original a. Saturation should be measured separately.

## Visual lesson

The codec visual displays action values and equal-width bins. Move a command through an interval to see its token change in steps while the decoded command stays at a bin center. A second action dimension can use different units and bounds. A table lists input, clipped value, bin ID, token and reconstruction error.

## Worked example

For l=−1, u=1 and B=4, the bin width is 0.5. Centers are −0.75, −0.25, 0.25 and 0.75. At a=0 the normalized position is 0.5, so floor(4×0.5)=2. The decoded command is 0.25. At a=1, floor(4)=4 must be clamped to bin 3.

## Why this matters on a robot

The policy and controller must share the codec version, unit conventions, bounds and token offset. A plausible token decoded with the wrong bounds can become an unsafe command. Freeze training-derived bounds with the checkpoint; do not recompute them on each episode. Monitor saturation rates and reconstruction error by dimension.

## Failure modes and scope

Off-by-one errors at the upper bound produce invalid vocabulary indices. Rounding instead of flooring moves decision boundaries. Uniform bins can waste vocabulary on rarely used ranges. Quantile codecs address a different tradeoff and must not be mixed silently with this uniform codec.

[RT-1](https://arxiv.org/abs/2212.06817) supplies the action-token motivation. Here the bounds are explicit inputs and no transformer, camera encoder or control loop is trained.
