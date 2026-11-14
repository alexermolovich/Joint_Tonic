# Roll Out Perturbed Control Sequences

## Intuition

A sampled control sequence is useful only after applying the system dynamics in order. Each candidate starts from the same observed state; its later states depend on its own earlier controls.

## Mathematics and conventions

For rollout k, step t, normalized state $x_{k,t}\in\mathbb R^D$, nominal command $u_t\in\mathbb R^U$ and supplied perturbation $\epsilon_{k,t}$,

$$v_{k,t}=u_t+\epsilon_{k,t},\qquad x_{k,0}=x_0,\qquad x_{k,t+1}=Ax_{k,t}+Bv_{k,t}.$$

Here $A\in\mathbb R^{D\times D}$ and $B\in\mathbb R^{D\times U}$ already encode the fixed controller period. The stated row-sum bound controls growth in the infinity norm. This rollout produces data for later cost evaluation; it does not select the best sequence or implement a complete MPPI update.

## Visual computation trace

| Step | Candidate 1 control/state | Candidate 2 control/state |
| --- | --- | --- |
| Initial | state 0 | state 0 |
| 0 | control 1 → state 1 | control 2 → state 2 |
| 1 | control 2 → state 3 | control 1 → state 3 |

## Worked examples

1. Scalar A=B=1, initial `[0.]`, nominal `[[1.],[2.]]`, one zero perturbation sequence yield controls `[[[1.],[2.]]]` and states `[[[0.],[1.],[3.]]]`.
2. The same inputs with perturbation sequence `[[[1.],[-1.]]]` yield controls `[[[2.],[1.]]]` and states `[[[0.],[2.],[3.]]]`.

## Why this matters on a robot

Sharing evolving state between candidates corrupts the comparison. A correct rollout under this linear model still says nothing about model mismatch on the physical robot.

## Source and prerequisites

[Primary paper](https://arxiv.org/abs/1509.01149). Read the typed contract and coordinate conventions above.

This static explanation has no animation; its tables and shape traces are the text equivalent of the computation.
