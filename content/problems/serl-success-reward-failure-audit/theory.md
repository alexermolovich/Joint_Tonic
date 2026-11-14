# Validate Success-Classifier Rewards on Robot Failures

## Intuition

A success classifier can be exploited if it mistakes recurring robot failures for completed tasks. Inspect false rewards by failure category instead of trusting only aggregate accuracy.

## Mathematical mechanism

With probability p, threshold tau, true success y and observed-valid mask M, define predicted success $\hat y=\mathbf1[p\ge\tau]$. The four global counts are $$TP=\sum_iM_iy_i\hat y_i,\quad FP=\sum_iM_i(1-y_i)\hat y_i,\quad FN=\sum_iM_iy_i(1-\hat y_i),\quad TN=\sum_iM_i(1-y_i)(1-\hat y_i).$$ Precision is TP/(TP+FP), recall TP/(TP+FN), with NaN on zero denominator. For failure category k, $$FPR_k=\frac{\sum_iM_i(1-y_i)\mathbf1[t_i=k]\hat y_i}{\sum_iM_i(1-y_i)\mathbf1[t_i=k]}.$$ Category labels t only identify actual failures; true successes carry -1. A missing category has unknown false-positive rate, not zero.

## Visual computation trace

| Observation | Probability | Threshold.5 result |
|---|---|---|
| True success | .9 | true positive |
| Failure type0 | .8 | false reward |
| Failure type1 | .2 | correctly rejected |

The table is the static visual and its text alternative; each row describes a transformation or decision.

## Worked calculation

For probabilities `[0.9, 0.8, 0.2]`, success labels `[True, False, False]`, failure types `[-1, 0, 1]`, all valid, threshold `0.5` and two failure types, return confusion `[1, 1, 0, 1]`, precision `0.5`, recall `1.0`, failure counts `[1, 1]`, false-positive counts `[1, 0]` and rates `[1.0, 0.0]`.

## Why this matters on a robot

A reward classifier can accidentally reward a visible failure, causing the learner to seek that failure. Aggregate precision can hide one failure category with many false positives; preserve per-category support and mark unobserved categories as unknown.

## Physical contract and limits

Normalized observation/action coordinates and reward probabilities are dimensionless. Interaction/reset durations use seconds. Counters and indices are exact integers. Transitions follow the caller-declared fixed control period within each recorded episode; no implicit clock or coordinate conversion. Scheduler ticks are accounting events, not a promised wall-clock cadence. Original bounded operational component motivated by SERL/HIL-SERL. It does not reproduce the entire learner, authorize physical robot execution or establish deployment safety.

Source: [primary paper](https://arxiv.org/abs/2401.16013). Prerequisite: understand the observation/action schema supplied in the contract; no additional lesson is required.
