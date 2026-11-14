# Aggregate Weighted Learner Gradients

## Intuition

Workers often process different numbers of valid transitions. Equal weight per worker changes the learning objective when their batch sizes differ.

## Formal model

For worker mean gradient $g_i\in\mathbb R^D$ and valid sample count $n_i\ge0$,
$$\bar g=\frac{\sum_i n_i g_i}{\sum_i n_i}.$$
Each gradient coordinate has normalized loss per normalized parameter units. A zero total has no learning evidence; its returned zero vector is accompanied by has_samples=False so it cannot be mistaken for measured convergence.

## Worked state and shape trace

```text
worker0:2samples*gradient1 ->2; worker1:6samples*gradient3 ->18; sum20/8=2.5.
```

The ordered text trace is also the visual alternative; no animation is required.

## Why this matters on a robot

Sensor padding and dropped frames can leave robot rollout workers with unequal valid batches. An unweighted average overrepresents small workers and can bias updates.

## Source and scope

Original bounded component inspired by [2017-rllib](https://arxiv.org/abs/1712.09381). It does not reproduce the full paper or establish hardware safety or data-use authorization.
