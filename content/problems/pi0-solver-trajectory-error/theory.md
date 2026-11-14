# Evaluate Solver Steps Against Trajectory Error

## Intuition

More solver steps spend time without guaranteeing a better predicted trajectory. Compare final chunks against one declared reference, then choose a candidate using measured latency only after its error satisfies the required limit.

## Mathematical mechanism

For candidate $\hat A^{(k)}\in\mathbb R^{H\times D}$ and common reference A, $$e_k=\sqrt{\frac1{HD}\sum_{h,d}(\hat A^{(k)}_{hd}-A_{hd})^2},\qquad m_k=\max_{h,d}|\hat A^{(k)}_{hd}-A_{hd}|.$$ Feasible candidates satisfy error and measured latency limits; lexicographic selection uses $(t_k,s_k,k)$. The reference is a declared fixture, not presumed physical ground truth.

## Visual computation trace

| Candidate | RMSE | latency ms | eligible |
|---|---|---|---|
| 0 | 1 | 2 | no if limit0.5 |
| 1 | 0 | 4 | yes if deadline4 |

The table is the static visual and its text alternative; each row describes a transformation or decision.

## Worked calculation

estimates=[[[1]],[[0]]],target=[[0]],steps=[1,4],latencies=[2,4],max_rmse=.5,deadline4 returns rmse[1,0],max_abs[1,0],feasible[False,True],selected_index1.

## Why this matters on a robot

A numerically plausible result can still represent the wrong action channel or calibration. Preserve preprocessing metadata and evaluate boundary behavior before closing the control loop.

## Physical contract and limits

Actions are normalized dimensionless; error same units; measured solver latency and deadline milliseconds; flow step count dimensionless. Caller-synchronized observations; generation time and physical control time are distinct. Original bounded engineering component motivated by the paper; no pretrained model or benchmark reproduction is implied.

Source: [primary paper](https://arxiv.org/abs/2410.24164v4). Prerequisite: understand the observation/action schema supplied in the contract; no additional lesson is required.
