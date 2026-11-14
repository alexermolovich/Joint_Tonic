# Reset Completed Environments Selectively

## Intuition

Only completed environments should restart. Continuing robots retain their state, episode identity and step count. Resetting a state row without advancing its episode ID can make downstream temporal windows cross an episode boundary.

## Mathematics and physical contract

State matrices $X,X^0\in\mathbb R^{B\times D}$ use matching per-column physical units and frames. With Boolean completion mask $m_b$, episode ID $e_b$ and step counter $t_b$,
$$X'_b=\begin{cases}X^0_b&m_b=1\\X_b&m_b=0,\end{cases}\quad e'_b=e_b+m_b,\quad t'_b=\begin{cases}0&m_b=1\\t_b&m_b=0.\end{cases}$$
Counters are dimensionless nonnegative int64 values; selected episode IDs must leave room for one increment. This is pure replacement, so continuing step counters do not advance. It performs no randomization, physics step or recurrent-policy memory reset.

## Worked pipeline and shape trace

```text
env  done  old state  reset state  episode  steps -> result
0    True   [1,2]      [0,0]         4      10 -> [0,0],5,0
1    False  [3,4]      [9,9]         8      20 -> [3,4],8,20
```

The text trace is the visual and accessible alternative; no animation is required.

## Why this matters on a robot

A batch-wide reset discards useful ongoing robot rollouts. Correct state replacement is only part of a real reset: policy memory, contact caches and sensors may need their own explicit handling in a simulator adapter.

## Prerequisites and source

The problem statement supplies the exact array, unit and boundary conventions. [Episode validity masks](/problems/build-robot-sequence-validity-masks) provide related context for preserving episode boundaries.

Original bounded component associated with [2021-isaac-gym](https://arxiv.org/abs/2108.10470). The scope and finite-sample or simulation conventions above are part of this exercise, not a claim of full-paper reproduction.
