# Compute an Adversarial Style Reward

## Intuition

AMP uses a least-squares discriminator score, not a probability. Its style reward peaks at the reference-motion label and decreases toward zero for scores far from that label.

## Mathematical mechanism

For real score D and Boolean validity M, $$r=M\max(0,1-\tfrac14(D-1)^2).$$ The score derivative is $-\tfrac12(D-1)$ only where M is true and the unclipped expression is strictly positive. Else use zero, including the clipping kinks D=-1 and D=3. Report the valid-sample mean, with zero for no valid samples. D and rewards are dimensionless. A bounded style reward does not calibrate physical safety, and replacing it with a sigmoid or log-GAN reward changes the algorithm.

## Visual computation trace

| Discriminator score | Style reward | Chosen score derivative |
|---|---|---|
| -1 | 0 | 0 at kink |
| 0 | 0.75 | +0.5 |
| 1 | 1 | 0 |
| 2 | 0.75 | -0.5 |
| 3 | 0 | 0 at kink |

The table is the static visual and its text alternative; each row describes a transformation or decision.

## Worked calculation

Scores [[-1, 0, 1, 2, 3]], all valid, yield rewards [[0, 0.75, 1, 0.75, 0]], score gradients [[0, 0.5, 0, -0.5, 0]] and mean_reward 0.5.

## Why this matters on a robot

A robot can receive a high imitation score while violating actuator or contact constraints. Inconsistent frame conventions or quaternion signs can also create artificial motion error.

## Physical contract and limits

Positions use meters, time seconds, angular quantities radians and rad/s; phase and reward are dimensionless. Exact per-input units appear in the contract. Synchronized motion states or phases are supplied. World coordinates are right-handed with +y up where used; local joint frames are relative to parents. Original bounded component using synthetic motion. No retargeting, discriminator or feedback policy is trained; no physical safety or full-paper reproduction claim.

Source: [primary paper](https://arxiv.org/abs/2104.02180). Prerequisite: understand the observation/action schema supplied in the contract; no additional lesson is required.
