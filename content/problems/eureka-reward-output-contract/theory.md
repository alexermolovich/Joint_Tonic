# Validate a Reward Function Contract

## Intuition

A reward callback needs a measurable interface before it can guide learning. Diagnose nonfinite values, excessive scale and inconsistent component totals without silently repairing the output.

## Mathematical mechanism

Let reward r have B rows and weighted component matrix C have shape B by K. For finite row i, define the reconstruction error $$d_i=\left|r_i-\sum_{k=1}^K C_{ik}\right|.$$ With magnitude bound b, tolerance epsilon and declared observation mask M, accept a row only when $$A_i=M_i\land F_i\land (|r_i|\le b)\land\bigwedge_k(|C_{ik}|\le b)\land(d_i\le\epsilon),$$ where F requires every reward/component value to be finite. All quantities are dimensionless. Missing rows still receive diagnostics but do not count as rejected valid evidence.

## Visual computation trace

| Captured result | Finite | Consistent | Decision |
|---|---|---|---|
| reward3, terms1+2 | yes | yes | accept if valid |
| reward3, terms1+1 | yes | no | reject if valid |
| rewardNaN | no | no | diagnose, never accept |

The table is the static visual and its text alternative; each row describes a transformation or decision.

## Worked calculation

rewards [3], components [[1,2]], valid [True], bound 3, atol 0 -> all flags True, invalid_count 0.

## Why this matters on a robot

A finite and well-scaled reward can still encourage the wrong behavior. Select policies with independent task and safety evidence; missing trials are not successful trials.

## Physical contract and limits

Reward contributions and independent progress/success metrics are dimensionless and already normalized. Observations are recorded rollout steps; paired comparisons share seed identity by column. No coordinate transform or simulator execution is implicit. Original bounded reward-design diagnostic or arithmetic teaching language. It does not reproduce language-model search, policy training or real-robot transfer.

Source: [primary paper](https://arxiv.org/abs/2310.12931). Prerequisite: understand the observation/action schema supplied in the contract; no additional lesson is required.
