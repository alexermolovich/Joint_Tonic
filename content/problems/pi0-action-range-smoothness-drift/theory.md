# Monitor Continuous-Action Range and Smoothness Drift

## Intuition

An action can stay inside its allowed range yet jump too quickly between control ticks. Track range and finite-difference speed separately, then count their union so a single bad sample does not contribute twice to the drift rate.

## Mathematical mechanism

For channel d and physical sample time $t_i$ seconds, $$v_{id}=|a_{id}-a_{i-1,d}|/(t_i-t_{i-1}),\quad F_{id}=R_{id}\lor[v_{id}>v_d^{max}],\quad r_d=T^{-1}\sum_iF_{id}.$$ Set the speed flag at i=0 to false, then drift is $r_d-r_d^{baseline}$. Rates use one denominator even when range and speed fail together; no double counting.

## Visual computation trace

| time s | action | range failure | speed failure |
|---|---|---|---|
| 0 | 0 | no | no |
| 1 | 2 | yes if max1 | yes if speed1 |
| 2 | 2 | yes | no |

The table is the static visual and its text alternative; each row describes a transformation or decision.

## Worked calculation

actions=[[0],[2],[2]],times=[0,1,2],bounds[0]..[1],speed[1],baseline[.5] returns range[False,True,True],speed[False,True,False],rate[2/3],drift[1/6].

## Why this matters on a robot

A numerically plausible result can still represent the wrong action channel or calibration. Preserve preprocessing metadata and evaluate boundary behavior before closing the control loop.

## Physical contract and limits

Normalized action units; timestamps seconds; max_speed normalized action units per second. Inputs must use the same normalization and controller frame as the baseline. Caller-synchronized observations; generation time and physical control time are distinct. Original bounded engineering component motivated by the paper; no pretrained model or benchmark reproduction is implied.

Source: [primary paper](https://arxiv.org/abs/2410.24164v4). Prerequisite: understand the observation/action schema supplied in the contract; no additional lesson is required.
