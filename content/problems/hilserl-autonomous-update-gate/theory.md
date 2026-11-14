# Gate an Online Policy Update

## Intuition

A candidate that succeeds only with human corrections has not shown autonomous improvement. Remove assisted trials from both policies before comparing the observed evaluation rates.

## Mathematical mechanism

For policy row k, observed-valid trials M and assisted flag H, evidence eligibility is $$E_{kj}=M_{kj}(1-H_{kj}),\quad n_k=\sum_jE_{kj},\quad s_k=\frac{\sum_jE_{kj}S_{kj}}{n_k},\quad v_k=\frac{\sum_jE_{kj}V_{kj}}{n_k}.$$ S is task success and V a separately recorded violation. A candidate passes only when its version is newer, both n meet the minimum, $s_1\ge s_0-\delta$ and $v_1\le v_{max}$. Missing rates fail the comparisons. These are point-estimate evidence checks, not confidence bounds or authority to execute a policy on hardware.

## Visual computation trace

| Candidate evaluation | Overall success | Eligible autonomous evidence |
|---|---|---|
| Two unassisted successes | 2/2 | two trials |
| Two assisted successes | 2/2 | zero trials, gate fails |

The table is the static visual and its text alternative; each row describes a transformation or decision.

## Worked calculation

Both policies have two valid autonomous trials. Success is `[[True, False], [True, True]]`, with no violations or assistance. Versions `1` and `2`, minimum trials `2`, allowed drop `0` and maximum violation rate `0` produce counts `[2, 2]`, success_rate `[0.5, 1]`, violation_rate `[0, 0]`, checks `[True, True, True, True]` and accepted `True`.

## Why this matters on a robot

Assistance can conceal a policy regression. A candidate with only assisted successes has no autonomous evidence, so comparisons stay false. These observed rates are an evaluation screen, not confidence bounds or permission to execute hardware.

## Physical contract and limits

Normalized observation/action coordinates and reward probabilities are dimensionless. Interaction/reset durations use seconds. Counters and indices are exact integers. Transitions follow the caller-declared fixed control period within each recorded episode; no implicit clock or coordinate conversion. Scheduler ticks are accounting events, not a promised wall-clock cadence. Original bounded operational component motivated by SERL/HIL-SERL. It does not reproduce the entire learner, authorize physical robot execution or establish deployment safety.

Source: [primary paper](https://arxiv.org/abs/2410.21845). Prerequisite: understand the observation/action schema supplied in the contract; no additional lesson is required.
