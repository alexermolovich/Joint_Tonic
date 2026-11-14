# Combine Motion and Task Rewards

## Intuition

A task score and a motion-quality score measure different properties. Keep their weighted contributions visible while producing the scalar reward used by a controller update.

## Mathematical mechanism

Let $r^m,r^g\in[0,1]^{B\times T}$ be supplied motion and goal rewards, M a Boolean validity mask, and nonnegative weights $w_m,w_g$. Compute $$c^m= M w_m r^m,\quad c^g=M w_g r^g,\quad r=c^m+c^g.$$ The reported mean divides the sum by the number of valid samples, not all padded entries. Empty support gives zero. Weights need not sum to one, so the combined reward need not remain in [0,1]. DeepMimic uses an imitation reward; AMP uses a learned style reward. Sharing this addition does not identify those underlying objectives.

## Visual computation trace

| Component | Input reward | Weight | Contribution |
|---|---|---|---|
| Motion | 0.8 | 0.75 | 0.6 |
| Task | 0.2 | 0.25 | 0.05 |
| Combined | aligned valid sample | sum | 0.65 |

The table is the static visual and its text alternative; each row describes a transformation or decision.

## Worked calculation

Motion reward [[0.8]], task reward [[0.2]], valid [[True]] and weights 0.75 and 0.25 produce contributions [[0.6]] and [[0.05]], reward [[0.65]] and mean_reward 0.65.

## Why this matters on a robot

A robot can receive a high imitation score while violating actuator or contact constraints. Inconsistent frame conventions or quaternion signs can also create artificial motion error.

## Physical contract and limits

Positions use meters, time seconds, angular quantities radians and rad/s; phase and reward are dimensionless. Exact per-input units appear in the contract. Synchronized motion states or phases are supplied. World coordinates are right-handed with +y up where used; local joint frames are relative to parents. Original bounded component using synthetic motion. No retargeting, discriminator or feedback policy is trained; no physical safety or full-paper reproduction claim.

Source: [primary paper](https://arxiv.org/abs/1804.02717). Prerequisite: understand the observation/action schema supplied in the contract; no additional lesson is required.

The shared weighted combination also appears in [AMP](https://arxiv.org/abs/2104.02180); its supplied motion reward is adversarial style rather than DeepMimic imitation.
