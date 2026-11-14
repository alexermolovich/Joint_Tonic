# Build Block Attention for VLM and Action Expert Tokens

## Intuition

The semantic context remains fixed while an action chunk is jointly refined. Context tokens can read each other, action tokens can read that context and the other actions, but context must not depend on the changing action tokens.

## Mathematical mechanism

With context presence c and action presence a, block visibility is $$R=\begin{bmatrix}\mathbf1_{C\times C}&\mathbf0_{C\times A}\\\mathbf1_{A\times C}&\mathbf1_{A\times A}\end{bmatrix},\qquad M_{bij}=R_{ij}p_{bi}p_{bj},\quad p=[c;a].$$ Queries index rows; keys index columns. Jointly denoised actions can interact at one flow time, while the VLM context stays independent of those changing actions.

## Visual computation trace

| Query | Context key | Action key |
|---|---|---|
| context | yes | no |
| action | yes | yes |

The table is the static visual and its text alternative; each row describes a transformation or decision.

## Worked calculation

context=[[True]], action=[[True,True]] gives mask[[[1,0,0],[1,1,1],[1,1,1]]] as booleans.

## Why this matters on a robot

A numerically plausible result can still represent the wrong action channel or calibration. Preserve preprocessing metadata and evaluate boundary behavior before closing the control loop.

## Physical contract and limits

Normalized actions and token features are dimensionless; physical calibration is supplied upstream. Caller-synchronized observations; generation time and physical control time are distinct. Original bounded engineering component motivated by the paper; no pretrained model or benchmark reproduction is implied.

Source: [primary paper](https://arxiv.org/abs/2410.24164v4). Prerequisite: understand the observation/action schema supplied in the contract; no additional lesson is required.
