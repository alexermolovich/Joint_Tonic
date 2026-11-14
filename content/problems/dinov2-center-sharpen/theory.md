# Center prototype scores, then control target sharpness

## Intuition

A teacher can favor one prototype across many images. A supplied center offsets per-prototype bias, while temperature controls how concentrated each target distribution becomes. These two operations affect different aspects of the target and should not be conflated.

## The probability transform

Let $Z\in\mathbb R^{B\times K}$ hold B teacher outputs over K prototypes. Let $c\in\mathbb R^K$ be the supplied center and $\tau>0$ the scalar temperature; all values are dimensionless. Define $A_{bk}=(Z_{bk}-c_k)/\tau$ and $m_b=\max_k A_{bk}$. Then

$$
P_{bk}=\frac{\exp(A_{bk}-m_b)}
{\sum_{j=1}^{K}\exp(A_{bj}-m_b)}.
$$

Subtracting the row maximum leaves softmax unchanged because the common exponential factor cancels. It prevents overflow. Underflow of a very unlikely prototype to zero is acceptable; every row still has at least one exponent equal to one.

## Visual: separate center and temperature

| Stage | Example row |
|---|---|
| Teacher scores | [2,0] |
| Subtract center [1,0] | [1,0] |
| Divide by temperature1 | [1,0] |
| Subtract maximum1 | [0,−1] |
| Normalize exponentials | [0.7310586,0.2689414] |

This numerical pipeline is also the text alternative. At temperature0.5, the centered margin doubles and the first probability rises to approximately0.8807971.

## Scope within the DINO family

The center is an input, not recomputed from the current batch. Estimating it here would silently change the algorithm and couple each target to all current examples. This bounded task studies the centering-and-sharpening variant; DINOv2's improved setup uses Sinkhorn-Knopp target balancing. Row softmax does not enforce balanced prototype usage across a batch.

In a training implementation, the teacher target is detached. This NumPy exercise has no autograd path and does not implement the teacher EMA or student cross-entropy.

## Why this matters on a robot

Collapsed prototype usage can hide poor representation diversity in camera data. Temperature alone cannot recover information missing from an encoder. Monitor feature and prototype distributions across environments, while keeping training-state versions distinct from deployed encoder weights.

## Questions and source

Why subtract a row maximum after centering? For numerical stability, not another learned correction. Does every prototype receive equal probability mass across B? No; rows normalize independently.

Source: [DINOv2 training discussion](https://arxiv.org/abs/2304.07193). The separate [EMA update](/problems/dinov2-teacher-ema) creates teacher parameters; it is not this target-distribution transform.
