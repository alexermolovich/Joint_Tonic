# Aggregate Reward-Component Diagnostics

## Intuition

A reward can be numerically valid yet be dominated by a constant or oversized component. Summarize observed terms and compare their variation with an independent progress signal.

## Mathematical mechanism

Flatten only valid episode/time observations into N samples. For component c, $$\mu_c=\frac1N\sum_i x_{ic},\quad\sigma_c=\sqrt{\frac1N\sum_i(x_{ic}-\mu_c)^2},\quad m_c=\frac1N\sum_i|x_{ic}|.$$ Let y be the independent task score with population mean and standard deviation mu_y and sigma_y. Pearson correlation is $$\rho_c=\frac{N^{-1}\sum_i(x_{ic}-\mu_c)(y_i-\mu_y)}{\sigma_c\sigma_y}.$$ A zero denominator yields NaN, not zero correlation. Missing support yields NaN for every statistic. These dimensionless sample diagnostics do not establish causation.

## Visual computation trace

| Term samples | Mean | Population std | Correlation with [0,1] |
|---|---|---|---|
| [1,3] | 2 | 1 | 1 |
| [2,2] | 2 | 0 | undefined |

The table is the static visual and its text alternative; each row describes a transformation or decision.

## Worked calculation

components [[[1,2],[3,2]]], scores [[0,1]], all valid -> mean [2,2], std [1,0], mean_abs [2,2], correlation [1,NaN], count 2.

## Why this matters on a robot

A finite and well-scaled reward can still encourage the wrong behavior. Select policies with independent task and safety evidence; missing trials are not successful trials.

## Physical contract and limits

Reward contributions and independent progress/success metrics are dimensionless and already normalized. Observations are recorded rollout steps; paired comparisons share seed identity by column. No coordinate transform or simulator execution is implicit. Original bounded reward-design diagnostic or arithmetic teaching language. It does not reproduce language-model search, policy training or real-robot transfer.

Source: [primary paper](https://arxiv.org/abs/2310.12931). Prerequisite: understand the observation/action schema supplied in the contract; no additional lesson is required.
