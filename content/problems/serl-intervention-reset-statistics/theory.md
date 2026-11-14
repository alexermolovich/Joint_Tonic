# Record Intervention and Reset Statistics

## Intuition

Training time, human effort and reset overhead describe different costs. Record them separately, and distinguish autonomous task outcomes from outcomes obtained with assistance.

## Mathematical mechanism

For observed trials with trial duration T_i, human duration H_i and reset duration R_i in seconds, $$T_{robot}=\sum_i(T_i+R_i),\quad T_{human}=\sum_iH_i,\quad T_{reset}=\sum_iR_i,\quad f_{human}=\frac{\sum_iH_i}{\sum_iT_i}.$$ Require 0<=H_i<=T_i. Human fraction is NaN when total trial duration is zero. Autonomous trial membership is exactly H_i=0, and autonomous success rate averages success only over those valid trials. Overall task and reset rates use all valid trials. Missing evidence never becomes a failed or successful trial.

## Visual computation trace

| Trial | Execution seconds | Human seconds | Reset seconds |
|---|---|---|---|
| 0 | 10 | 0 | 2 |
| 1 | 20 | 5 | 3 |
| Totals | 30 | 5 | 5 |

The table is the static visual and its text alternative; each row describes a transformation or decision.

## Worked calculation

Trial durations `[10, 20]`, human durations `[0, 5]`, reset durations `[2, 3]`, task success `[True, True]`, reset success `[True, False]`, all valid: trials `2`, autonomous_trials `1`, robot_time `35`, human_time `5`, reset_time `5`, human_fraction `1/6`, task_success_rate `1`, reset_success_rate `0.5` and autonomous_success_rate `1`.

## Why this matters on a robot

A policy may look fast if reset time or human effort is omitted. Count execution and reset time separately, and keep assisted successes out of the autonomous rate. Zero observed trials is missing evidence rather than a measured failure rate.

## Physical contract and limits

Normalized observation/action coordinates and reward probabilities are dimensionless. Interaction/reset durations use seconds. Counters and indices are exact integers. Transitions follow the caller-declared fixed control period within each recorded episode; no implicit clock or coordinate conversion. Scheduler ticks are accounting events, not a promised wall-clock cadence. Original bounded operational component motivated by SERL/HIL-SERL. It does not reproduce the entire learner, authorize physical robot execution or establish deployment safety.

Source: [primary paper](https://arxiv.org/abs/2401.16013). Prerequisite: understand the observation/action schema supplied in the contract; no additional lesson is required.
