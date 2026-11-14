# Quantize Actions from Training-Set Quantiles

## Intuition

Rare training outliers should not consume most action-bin resolution. Fit robust bounds from training data, then divide that interval into equal-width bins; changing the evaluation actions must never change those bounds.

## Mathematical mechanism

For sorted training channel $x_{(i)}$, the linear q-quantile uses $h=(N-1)q$, $k=\lfloor h\rfloor$, and $Q_q=(1-h+k)x_{(k)}+(h-k)x_{(k+1)}$. Bounds are $l=Q_{.01}$ and $u=Q_{.99}$. $$z=\operatorname{clip}\left(\left\lfloor K\operatorname{clip}\left(\frac{a-l}{u-l},0,1\right)\right\rfloor,0,K-1\right),\quad \hat a=l+(z+1/2)(u-l)/K.$$ All operations are channelwise; K is supplied bin count, not vocabulary size.

## Visual computation trace

| Stage | Channel example |
|---|---|
| train | [0,100] |
| percentile bounds | [1,99] |
| K=2 width | 49 |
| centers | 25.5,74.5 |

The table is the static visual and its text alternative; each row describes a transformation or decision.

## Worked calculation

Training=[[0],[100]], actions=[[0],[50],[100]], bins2 returns lower[1], upper[99], codes[[0],[1],[1]], decoded[[25.5],[74.5],[74.5]].

## Why this matters on a robot

A numerically plausible result can still represent the wrong action channel or calibration. Preserve preprocessing metadata and evaluate boundary behavior before closing the control loop.

## Physical contract and limits

Normalized actions and token features are dimensionless; physical calibration is supplied upstream. Caller-synchronized observations; generation time and physical control time are distinct. Original bounded engineering component motivated by the paper; no pretrained model or benchmark reproduction is implied.

Source: [primary paper](https://arxiv.org/abs/2406.09246). Prerequisite: understand the observation/action schema supplied in the contract; no additional lesson is required.
