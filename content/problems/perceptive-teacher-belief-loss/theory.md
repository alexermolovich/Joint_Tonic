# Compute Belief Reconstruction and Teacher-Action Losses

## Intuition

A student can imitate a teacher action even when some environmental labels are unavailable. Keep action supervision and belief reconstruction separate, normalize each by its own physical scale, and expose both counts so missing labels cannot silently change the objective.

## Mathematical mechanism

Let student and fixed teacher actions $a,\bar a\in\mathbb R^{B\times T\times A}$ use radians in matching joint order. Let reconstruction and fixed privileged target $z,\bar z\in\mathbb R^{B\times T\times D}$ use normalized environmental coordinates. Boolean $M\in\{0,1\}^{B\times T}$ selects whole action vectors; $N\in\{0,1\}^{B\times T\times D}$ selects individual environmental labels. Positive channel scales $s\in\mathbb R^A$ and $u\in\mathbb R^D$ have the same units as their respective targets. Define the eligible scalar counts and dimensionless losses:
$$n_a=A\sum_{bt}M_{bt},\qquad n_z=\sum_{btd}N_{btd},$$
$$L_a=\frac{1}{n_a}\sum_{bti}M_{bt}\left(\frac{a_{bti}-\bar a_{bti}}{s_i}\right)^2,\qquad L_z=\frac{1}{n_z}\sum_{btd}N_{btd}\left(\frac{z_{btd}-\bar z_{btd}}{u_d}\right)^2.$$
An absent component has loss zero rather than fabricated targets. With fixed nonnegative dimensionless weights $w_0,w_1$, $L=w_0L_a+w_1L_z$. The requested gradients are with respect to student predictions only:
$$\frac{\partial L}{\partial a_{bti}}=\frac{2w_0M_{bt}(a_{bti}-\bar a_{bti})}{n_a s_i^2},\qquad \frac{\partial L}{\partial z_{btd}}=\frac{2w_1N_{btd}(z_{btd}-\bar z_{btd})}{n_z u_d^2}.$$
Define each absent-component gradient as zero. Action gradients have inverse-radian units; feature gradients have inverse-normalized-coordinate units. Dividing by only one power of the scale gives the wrong derivative. This scale-normalized masked objective is an original teaching contract, not a claim about the paper's exact loss weights.

## Visual computation trace

| Branch | Eligible unit | Denominator | Output |
|---|---|---|---|
| Teacher actions | Every joint of an eligible time row | A Ã— valid row count | Action MSE and student-action gradient |
| Privileged reconstruction | Individually observed feature element | Observed element count | Feature MSE and reconstruction gradient |
| Weighted sum | Two independently normalized components | No pooled count | Total loss |

The table is the static visual and its text alternative; each row describes a transformation or decision.

## Worked calculation

Use `B=T=A=D=1`: student action `[[[1.]]]`, teacher action `[[[0.]]]`, reconstruction `[[[2.]]]`, target `[[[0.]]]`, both masks true, `action_scale=[2.]`, `feature_scale=[1.]`, and `weights=[2.,0.5]`.

The action error is `(1/2)^2 = 0.25`; the reconstruction error is `2^2 = 4`. Return `components=[0.25,4.]`, `counts=[1,1]`, `loss=2.5`, `action_gradient=[[[1.]]]`, and `reconstruction_gradient=[[[2.]]]`.

## Why this matters on a robot

Missing terrain labels should not dilute action supervision. Pooling the two masks changes the effective weights as observations disappear. A low distillation loss alone does not verify robust closed-loop behavior on unseen terrain.

## Physical contract and limits

Action targets and action scales use radians. Environmental features and their scales share declared normalized coordinates. Foot positions, terrain heights and clearance thresholds use meters; resulting normalized losses and violation rates are dimensionless. Times are already aligned within each environment. A terrain label is constant across one supplied window. No resampling, recurrent state estimation or simulator stepping occurs. Original bounded teacher/student objective or terrain diagnostic associated with perceptive locomotion; no claim to reproduce the paper's recurrent gated network, training weights or hardware performance. All fixtures are synthetic.

Source: [primary paper](https://arxiv.org/abs/2201.08117). Prerequisite: understand the observation/action schema supplied in the contract; no additional lesson is required.
