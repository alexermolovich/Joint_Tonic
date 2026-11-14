# Gate Sim-to-Real Release with Robustness Evidence

## Intuition

A pooled score can hide an untested safety-relevant scenario. Require explicit evidence for every declared slice and verify that all rows describe the intended simulation distribution.

## Conjunctive evidence checks

For required slice b, let n_b be trial count, k_b successes, w_b worst normalized return, and d_b distribution digest. Given thresholds n_min,p_min,w_min and intended digest d*, approval requires

$$G_b=(d_b=d^*)\land(n_b\ge n_{min})\land(k_b/n_b\ge p_{min})\land(w_b\ge w_{min}).$$

Overall approval is the conjunction over every required slice, with any missing slice false. Counts are positive integers; rates and returns are dimensionless, comparable across slices. Emit all failures rather than stopping at the first so reviewers can distinguish stale evidence from poor performance.

## Visual release checklist

| Slice | Distribution | Trials | Success | Worst return | Result |
|---|---|---|---|---|---|
| low_light | matches | 10>=10 | 8/10>=0.8 | -1>=-1 | pass |
| high_delay | missing | unknown | unknown | unknown | missing |

Overall approval is false. The static table is the visual and text alternative; equality at each declared threshold passes.

## Why this matters on a robot

Evidence from an older dynamics distribution may not support a new calibration envelope. This gate deliberately checks declared summaries, so tampered summaries or unrepresentative trials can still pass. Hardware testing, confidence analysis, coupled safety constraints and authenticated provenance are separate requirements.

Prerequisites: [Estimate Scenario Coverage and Confidence Intervals](/problems/scenario-coverage-confidence), [Aggregate Mean and Worst-Case Policy Returns](/problems/aggregate-policy-returns).

## Source and scope

This original bounded component is motivated by [2018-dynamics-randomization](https://arxiv.org/abs/1710.06537). It does not reproduce the full paper, trained model or benchmark protocol.
