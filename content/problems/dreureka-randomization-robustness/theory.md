# Compare Robustness Across Randomization Settings

## Intuition

A physics setting can appear stronger merely because it was tested on easier rollout seeds. Compare the same observed seed columns when measuring degradation against a baseline.

## Mathematical mechanism

Let S_gj be Boolean task success and M_gj observation validity for setting g and seed j. With baseline row b, paired support is $$P_{gj}=M_{gj}\land M_{bj},\quad n_g^{pair}=\sum_jP_{gj},\quad\Delta_g=\frac{\sum_jP_{gj}(S_{gj}-S_{bj})}{n_g^{pair}}.$$ Cast success labels to signed numeric values before subtraction. No pairs gives NaN; too few pairs makes the setting incomparable. The worst comparable setting minimizes delta, with row index breaking ties. Separate raw success rates use all observed trials and therefore need not preserve the paired ranking.

## Visual computation trace

| Seed | Baseline | Setting1 | Difference |
|---|---|---|---|
| 0 | success | fail | -1 |
| 1 | fail | fail | 0 |
| Paired mean | two shared trials | same seeds | -.5 |

The table is the static visual and its text alternative; each row describes a transformation or decision.

## Worked calculation

success [[True,False],[False,False]], all valid, baseline 0,min_pairs 2 -> success_rate [.5,0], paired_delta [0,-.5], worst_index 1.

## Why this matters on a robot

A finite and well-scaled reward can still encourage the wrong behavior. Select policies with independent task and safety evidence; missing trials are not successful trials.

## Physical contract and limits

Reward contributions and independent progress/success metrics are dimensionless and already normalized. Observations are recorded rollout steps; paired comparisons share seed identity by column. No coordinate transform or simulator execution is implicit. Original bounded reward-design diagnostic or arithmetic teaching language. It does not reproduce language-model search, policy training or real-robot transfer.

Source: [primary paper](https://arxiv.org/abs/2406.01967). Prerequisite: understand the observation/action schema supplied in the contract; no additional lesson is required.
