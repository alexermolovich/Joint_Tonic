# Stable Softmax for Masked Sequences

## Intuition

A missing sensor token should receive no attention, while a large score should not overflow the computation. An entirely missing sequence has no probability distribution to normalize, so this contract returns a zero row and leaves fallback handling to the policy.

## Normalize only available evidence

For row $b$, valid indices form $V_b$. If nonempty, choose $m_b=\max_{j\in V_b}z_{bj}$ and compute

$$p_{bj}=\frac{\exp(z_{bj}-m_b)}{\sum_{k\in V_b}\exp(z_{bk}-m_b)},\quad j\in V_b.$$

Masked entries are zero. $z$ is dimensionless, $p$ is a dimensionless probability, $B$ indexes contexts and $L$ token positions. Every exponent used is nonpositive, so the largest exponentiated value is 1. For empty $V_b$ the output is zero by explicit policy, not an ordinary softmax distribution.

## Visual numerical trace

| Scores | Mask | Valid maximum | Output |
|---|---|---|---|
| [1000,1000,-1000] | [true,true,false] | 1000 | [0.5,0.5,0] |
| [1,2,3] | [false,false,false] | none | [0,0,0] |

This static trace also supplies the text alternative.

## Why this matters on a robot

Using a masked high score when choosing the maximum can underflow every valid exponential. Normalizing an all-masked row can generate NaNs that spread through an action head. A zero row must trigger an explicit downstream missing-context policy rather than be treated as confident evidence.

Prerequisite: [Broadcast Batched Sensor Features](/problems/broadcast-batched-sensor-features).

## Source and scope

Original robotics evaluation exercise. [NumPy reference](https://numpy.org/doc/2.2/reference/) documents the array operations; the physical contract and synthetic examples are original.
