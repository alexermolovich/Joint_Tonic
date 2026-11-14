# Validate Missing-Modality and Stale-Sensor Inputs

## Intuition

A tensor with the right shape may still describe the robot’s past. Presence and freshness are separate facts, and a policy should specify which sensors are essential before deciding whether to issue an action.

## Mathematical mechanism

Let P be presence, s sensor timestamps, t current time, and a maximum ages. For each batch b and modality m, $$S_{bm}=P_{bm}\land[(s_{bm}>t_b)\lor(t_b-s_{bm}>a_m)],\quad U_{bm}=P_{bm}\land\neg S_{bm}.$$ With required mask R, readiness is $G_b=\bigwedge_m(\neg R_m\lor U_{bm})$. Future timestamps fail freshness instead of producing a misleading negative age.

## Visual computation trace

| Sensor | Present | Timestamp/current | Limit | Usable |
|---|---|---|---|---|
| camera | true | 9/10s | 1s | true |
| state | true | 8/10s | 1s | false |

The table is the static visual and its text alternative; each row describes a transformation or decision.

## Worked calculation

present=[[True,True]], timestamps=[[9,8]], now=[10], max_age=[1,1], required=[True,True] returns usable=[[True,False]], stale=[[False,True]], ready=[False].

## Why this matters on a robot

A future timestamp may mean a clock mismatch rather than a fresh measurement. Optional sensors can be unavailable without blocking the declared gate, but downstream models must actually support that missingness. Silent imputation would change the policy interface.

## Physical contract and limits

All timestamps and ages are seconds on one synchronized clock; sensors retain caller-declared calibration/frame. Boundary age=max_age is usable; future sensor stamps are not usable. No clock correction is performed. Original deployment input gate motivated by embodied multimodal models. It does not impute a missing modality or establish spatial calibration validity.

Source: [primary paper](https://arxiv.org/abs/2303.03378). Prerequisite: understand the observation/action schema supplied in the contract; no additional lesson is required.
