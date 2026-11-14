# Quantize and Decode Robot Actions

A language-model-style policy emits integer tokens, while a controller consumes real-valued joint or end-effector commands. Build a deterministic codec that clips each action dimension to its declared bounds, converts it into a uniform bin token, and reconstructs the bin center.

~~~python
action_codec(actions, lower, upper, bins=256, token_offset=0)
# -> (tokens, decoded)
~~~

## Contract

Convert actions to float64 with shape (...,D), where D ≥ 1. lower and upper must be vectors of shape (D,). Bounds and actions must be finite, every upper bound must exceed its lower bound, and their difference must remain finite. Scalars are not action arrays. Empty leading dimensions, such as (0,D), are allowed.

bins must be an integer ≥ 2; token_offset must be an integer ≥ 0. Boolean values do not count as integers. The largest token must fit in signed int64.

For each dimension, clip the action to [lower,upper], scale to [0,1], calculate floor(bins×scaled), and clip the bin index to bins−1 at the upper endpoint. Return int64 tokens after adding token_offset. Return float64 decoded values at bin centers. Both outputs preserve the action shape; the inputs remain unchanged.

Bounds have the same physical unit as their respective action dimension. For example, a position dimension may use meters while a rotation dimension uses radians; never combine their statistics.

## Examples

**Example 1 — endpoints**

~~~python
actions = [[-1.], [0.], [1.]]
tokens, decoded = action_codec(actions, [-1.], [1.], bins=4)
# tokens:  [[0], [2], [3]]
# decoded: [[-0.75], [0.25], [0.75]]
~~~

Zero lies exactly on the boundary between bins 1 and 2 and goes into the upper bin. The upper bound maps to the last valid bin.

**Example 2 — clipping and reserved token IDs**

~~~python
tokens, decoded = action_codec([[-5., 9.]], [0., 0.], [2., 8.],
                               bins=2, token_offset=100)
# tokens:  [[100, 101]]
# decoded: [[0.5, 6.0]]
~~~

The first command is clipped to 0 and the second to 8. The reserved offset changes token IDs but does not alter decoded physical values.

## Errors

Raise TypeError for noninteger bins or token_offset. Raise ValueError for invalid counts/offsets, int64 token overflow, nonnumeric/nonfinite arrays, wrong shapes, or invalid bounds. Grading tolerates floating error at 1e−7; do not add arbitrary epsilons that move exact bin boundaries.

## Hints

- Use separate lower/upper values for every action dimension.
- The decoded value is the center, not the left edge.
- Never infer bounds from evaluation inputs.

Source: [RT-1](https://arxiv.org/abs/2212.06817). This is a small uniform-bin teaching codec; it does not reproduce the entire policy or its deployment interface.
