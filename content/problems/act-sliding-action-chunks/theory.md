# Build Sliding Action Chunks with Padding Masks: theory

## Intuition

An action-chunk policy predicts several future commands from one observation. Training therefore needs a window beginning at that observation’s control tick. Near an episode boundary, only part of the future exists. A mask distinguishes that missing future from a real command whose numeric value happens to be zero.

## Window indices and physical time

Let the episode have $T$ action rows and $D$ channels, $A\in\mathbb R^{T\times D}$. Requested starts are $s_i$ for $i=0,\ldots,S-1$, and horizon length is $H$. Define

$$
j_{ih}=s_i+h,\qquad M_{ih}=\mathbf1[j_{ih}<T],
$$

$$
C_{ihd}=\begin{cases}A_{j_{ih},d}&M_{ih}=1,\\0&M_{ih}=0.\end{cases}
$$

Indices are control ticks. If the caller’s control period is $\Delta t$ seconds, the target at offset $h$ belongs to time $(s_i+h)\Delta t$ relative to the episode start. This function does not resample irregular timestamps or infer the controller rate.

## Why padding needs a separate mask

A valid command may be zero: holding zero velocity is ordinary behavior. Therefore $M$ must come from episode indices, never from testing whether $C$ is nonzero. Repeating the final action would represent a different target-construction contract. Zero padding is convenient only because a later masked loss removes its influence.

A future elementwise squared-error objective would divide by the number of valid action scalars,

$$
L=\frac{\sum_{i,h,d}M_{ih}(\hat C_{ihd}-C_{ihd})^2}{D\sum_{i,h}M_{ih}}.
$$

This equation explains how validity is consumed; calculating that loss is outside this extraction task. An empty requested-window batch is valid here but would require skipping or rejecting a loss with zero denominator.

## Worked calculation

For $A=(1,2,3)$, $H=2$, and starts $(0,2)$, index rows are $(0,1)$ and $(2,3)$. Only index3 is outside the episode, producing chunks $(1,2)$ and $(3,0)$ with masks $(1,1)$ and $(1,0)$. The output does not borrow the first action of a following episode.

## Original index diagram

| Requested start | Offset 0 | Offset 1 | Offset 2 |
|---|---|---|---|
| 0 in a 3-step episode | action[0], valid | action[1], valid | action[2], valid |
| 2 in a 3-step episode | action[2], valid | zero, invalid | zero, invalid |

Columns are future offsets from each row's requested start; rows never cross episode boundaries.

Text alternative: the first requested window reads the first two recorded rows. The second reads the last row and then missing data. Only the missing slot receives zero padding and False validity.

## Why this matters on a robot

Crossing an episode boundary can pair a late grasp observation with the next episode’s reset action. A model may learn an abrupt movement that never occurred in the demonstration. Preserve episode identity, action order, controller units, and the mask when storing chunks. Avoid aliasing the dataset: changing a training window must not silently modify future examples.

## Check your understanding

1. Why must a real all-zero action still have a True validity entry?
2. For an episode of length5, start3, and horizon4, which target indices are valid?
3. Why is it incorrect to take missing tail entries from the next episode in a concatenated dataset?

## Sources and prerequisites

[Primary paper](https://arxiv.org/abs/2304.13705). ACT motivates predicting future action chunks. This exercise only builds supervised target windows from one recorded episode. Zero right-padding and True=valid masks are explicit educational conventions; no CVAE, policy inference, or cross-episode concatenation is implemented.

- [validate-robot-episodes](/problems/validate-robot-episodes)
