# Build a VLA Action-Token Training Batch

## Intuition

A robot policy should learn action tokens without being asked to reconstruct its instruction as part of this objective. Preserve the full prompt as context, supervise only actions and EOS, and distinguish padding from tokens that happen to share ordinary values.

## Mathematical mechanism

For prompt length $P_b$ and action length $A_b$, sequence length $L_b=P_b+A_b+1$. $$y_{bi}=\begin{cases}x_{bi},&P_b\le i<L_b,\\-100,&\text{otherwise}.\end{cases}$$ The last valid token is EOS. Attention mask is $i<L_b$; a separate causal mask controls direction. The loss aligns prediction at i-1 with label at i, so this collator must not pre-shift labels.

## Visual computation trace

| Token | prompt7 | action8 | EOS1 | padding0 |
|---|---|---|---|---|
| label | -100 | 8 | 1 | -100 |
| present | true | true | true | false |

The table is the static visual and its text alternative; each row describes a transformation or decision.

## Worked calculation

prompts=[[7],[6,7]], actions=[[8],[9]], pad0,eos1,vocab10 gives inputs[[7,8,1,0],[6,7,9,1]], labels[[-100,8,1,-100],[-100,-100,9,1]], lengths[3,4].

## Why this matters on a robot

A numerically plausible result can still represent the wrong action channel or calibration. Preserve preprocessing metadata and evaluate boundary behavior before closing the control loop.

## Physical contract and limits

Normalized actions and token features are dimensionless; physical calibration is supplied upstream. Caller-synchronized observations; generation time and physical control time are distinct. Original bounded engineering component motivated by the paper; no pretrained model or benchmark reproduction is implied.

Source: [primary paper](https://arxiv.org/abs/2406.09246). Prerequisite: understand the observation/action schema supplied in the contract; no additional lesson is required.
