# Compute an Adversarial Style Reward

AMP uses a least-squares discriminator score, not a probability. Its style reward peaks at the reference-motion label and decreases toward zero for scores far from that label.

## Contract

`scores` is real `(B, T)`, with `1 <= B <= 128`, `1 <= T <= 256` and absolute values at most 100. `valid` is Boolean with the same shape.

Return a dictionary containing:

- `reward`: float64 `(B, T)`, equal to `max(0, 1 - 0.25*(score-1)**2)` at valid entries and zero elsewhere.
- `score_gradient`: float64 `(B, T)`, equal to `-0.5*(score-1)` only where the sample is valid and the unclipped reward is strictly positive; zero elsewhere. Choose zero at the clipping kinks, scores -1 and 3.
- `mean_reward`: Python float, the valid-sample mean, or zero if no sample is valid.

Scores are real least-squares discriminator outputs, not probabilities. Do not substitute a sigmoid or logarithmic GAN reward. This function does not train a discriminator or implement its gradient penalty.

Unless a tighter bound is stated below, numeric array-like inputs must have real integer/floating dtype after `np.asarray`, be finite with absolute values <=1e6 and at most 1,000,000 entries. Boolean, complex, string and object numeric arrays are invalid; Boolean masks must have Boolean dtype. Integer arrays/scalars exclude booleans. All invalid inputs raise ValueError. Return new arrays, preserve inputs, and compute floating outputs in float64 on CPU. No automatic differentiation is required.

## Physical context and scope

Positions use meters, time seconds, angular quantities radians and rad/s; phase and reward are dimensionless. Exact per-input units appear in the contract. Synchronized motion states or phases are supplied. World coordinates are right-handed with +y up where used; local joint frames are relative to parents. Original bounded component using synthetic motion. No retargeting, discriminator or feedback policy is trained; no physical safety or full-paper reproduction claim.

## Example 1

Scores [[-1, 0, 1, 2, 3]], all valid, yield rewards [[0, 0.75, 1, 0.75, 0]], score gradients [[0, 0.5, 0, -0.5, 0]] and mean_reward 0.5.

## Example 2

Score 4 yields reward 0 and gradient 0. An invalid score 0 also yields zero reward and gradient; an entirely invalid batch has mean_reward 0.
