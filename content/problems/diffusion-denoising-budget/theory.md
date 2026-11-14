# Budget Denoising Steps Against Control Frequency

## Intuition

More denoising iterations can improve a sampler while missing a robot deadline. Separate a measured cost model from the policy-quality question and choose only among candidates that fit the control period.

## Mathematical mechanism

Let S_i be candidate denoising counts, c positive measured milliseconds per step, o fixed overhead, and f control frequency in Hz. The period is 

$$P=1000/f$$

 ms and candidate cost is $L_i=o+cS_i$. Feasible means $L_i\leq P$. Select the largest feasible S_i, not the last array element. A zero result denotes no feasible plan.

## Visual computation trace

| Steps | Cost with2ms/step+1ms | Within10ms? |
|---|---|---|
| 1 | 3ms | yes |
| 4 | 9ms | yes |
| 5 | 11ms | no |

The table is the static visual and its text alternative; each row describes a transformation or decision.

## Worked calculation

candidate_steps=[1,4,5], step_ms=2, overhead_ms=1, frequency_hz=100 returns latency_ms=[3,9,11], feasible=[True,True,False], selected_steps=4.

## Why this matters on a robot

Mean inference time can understate tail latency. Supply a cost estimate appropriate to the deadline, record the hardware/runtime, and evaluate action quality separately. This arithmetic cannot guarantee end-to-end timing under queueing or changing sensor load.

## Physical contract and limits

Latency milliseconds; control frequency Hertz; counts dimensionless. One planning invocation per period1000/frequency_hz ms; overlap or amortization across action windows is outside this task. Original serving-budget exercise inspired by Diffusion Policy inference scheduling. A constant measured per-step cost is an explicit approximation, not a published timing guarantee.

Source: [primary paper](https://arxiv.org/abs/2303.04137). Prerequisite: understand the observation/action schema supplied in the contract; no additional lesson is required.
