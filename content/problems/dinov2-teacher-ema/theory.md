# Theory

## Intuition: let the target change more slowly than the learner

In teacher-student self-supervision, a student learns from targets supplied by a teacher. Copying the student after every update makes the teacher change just as abruptly; freezing it forever prevents it from following learning. Exponential moving average provides an intermediate behavior: the teacher moves partway toward the new student parameters on each step.

This operation updates parameter values, not predicted probabilities. Target normalization, centering, sharpening, and the self-supervised loss are separate mechanisms. EMA alone does not prevent collapsed representations or make every training setup stable.

## Define one update and its timing

Let $\theta_T^{(k-1)}$ be the previous teacher parameters and $\theta_S^{(k)}$ the student **after** optimizer step $k$. Tensor correspondence is determined by parameter name. A scalar momentum $\mu\in[0,1]$ gives

$$
\theta_T^{(k)}=\mu\theta_T^{(k-1)}+(1-\mu)\theta_S^{(k)}.
$$

The equation applies elementwise within identically shaped tensor pairs. Momentum is dimensionless, and $k$ counts updates rather than physical time. Using the pre-step student changes the update's timing and does not satisfy this contract.

For constant momentum and $k$ updates, expansion yields

$$
\theta_T^{(k)}=\mu^k\theta_T^{(0)}+
(1-\mu)\sum_{j=1}^{k}\mu^{k-j}\theta_S^{(j)}.
$$

Older student snapshots receive geometrically decreasing weight. The initial teacher retains weight $\mu^k$. There is no bias-correction division in this contract. Real training can schedule momentum, but a single call receives only its current value.

## Worked update and visual

With teacher `[2,4]`, student `[6,0]`, and $\mu=0.9$, the new teacher is `[2.4,3.6]`. If the next post-step student is `[0,8]`, a second update gives `[2.16,4.04]`. This is different from averaging only the latest two students; the older teacher remains represented.

| Parameter | Old teacher | Post-step student | Momentum | New teacher |
|---|---|---|---:|---|
| weight | [2,4] | [6,0] | 0.9 | [2.4,3.6] |
| bias | 1 | 3 | 0.9 | 1.2 |

Pair rows by parameter name, independent of dictionary order. The new column is a detached snapshot used by the next teacher pass.

Text alternative: the optimizer first changes the student; then the EMA combines that snapshot with the previous teacher using matching names. The result is a new teacher snapshot without a backward connection. Both source dictionaries remain unchanged. The caller decides when to install the returned parameters.

## Why this matters on a robot

When training perception on new camera domains, reproducibility requires the teacher checkpoint, student checkpoint, momentum schedule, and global step. Restoring only the student changes future teacher targets. A key-order bug can combine unrelated tensors whose shapes happen to match; pairing by name prevents this silent error.

Do not pass integer counters or normalization buffers into a parameter-only function. Full-model buffer policy is architecture-specific and belongs in a later integration exercise. This task also checks that disabling teacher gradients does not accidentally mutate or detach the student's own training tensors.

Source: [DINOv2 section 3](https://arxiv.org/abs/2304.07193) and the official [`update_teacher` mechanism](https://github.com/facebookresearch/dinov2/blob/main/dinov2/train/ssl_meta_arch.py). The pure snapshot API is an original teaching boundary; it does not reproduce distributed training, centering, Sinkhorn normalization, or the full DINOv2 objective.

## Check your understanding

1. What goes wrong if two same-shaped parameter dictionaries are paired by iteration order?
2. At momentum1, may the function return the original teacher dictionary?

Discuss these after working through the numerical example. Answers are in [examples.md](#).
