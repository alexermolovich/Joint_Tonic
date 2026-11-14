# Encode Symlog Two-Hot Reward Targets

## Intuition

A signed logarithm compresses large reward magnitudes without losing their sign. Two neighboring bins preserve the transformed value by interpolation instead of abruptly rounding it to one class.

## Mathematical mechanism

For scalar reward x on the declared normalized scale, $$y=\operatorname{sign}(x)\log(1+|x|),\qquad\operatorname{symexp}(y)=\operatorname{sign}(y)(e^{|y|}-1).$$ Clip y to the supplied increasing support. If adjacent centers satisfy b_l<=y<=b_h, assign $$w_l=\frac{b_h-y}{b_h-b_l},\quad w_h=\frac{y-b_l}{b_h-b_l},\quad w_l+w_h=1.$$ Exact centers and clipped endpoints are one-hot. Recover the bounded target with symexp of the weighted bin mean, not a weighted average of symexp of individual bins. Targets have shape N by K; reconstruction has shape N.

## Visual computation trace

| Raw reward | Symlog value | Bins[-1,0,2] target |
|---|---|---|
| 0 | 0 | [0,1,0] |
| exp(1)-1 | 1 | [0,.5,.5] |

The table is the static visual and its text alternative; each row describes a transformation or decision.

## Worked calculation

Rewards[0,exp(1)-1], bins[-1,0,2] -> symlog[0,1], targets[[0,1,0],[0,.5,.5]], reconstructed equals supplied rewards.

## Why this matters on a robot

Errors in learned contact dynamics or termination predictions can compound through an imagined horizon. A numerically correct return remains conditional on those supplied predictions.

## Physical contract and limits

Latents and normalized actions are dimensionless. Rewards/values use a fixed caller-declared dimensionless reward scale; KL is measured in nats. Each ordered index is one fixed caller-declared control interval. Predicted continuation is a probability, not an elapsed duration. No implicit frame conversion. A bounded component with supplied tensors. Prediction loss inputs and deterministic imagined dynamics do not reproduce the complete trained recurrent stochastic world model, actor or benchmark.

Source: [primary paper](https://arxiv.org/html/2301.04104v2). Prerequisite: understand the observation/action schema supplied in the contract; no additional lesson is required.
