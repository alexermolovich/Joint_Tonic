# Build Lambda-Return Targets

## Intuition

An imagined transition may continue only with some predicted probability. Multiply the bootstrapped future by that probability while preserving the immediate reward and a clear final-step bootstrap.

## Mathematical mechanism

Let r_bt be reward, Vnext_bt the value at the successor state, c_bt a continuation probability, gamma the discount and lambda the trace mixing coefficient. Then $$G_{bt}=r_{bt}+\gamma c_{bt}\left[(1-\lambda)V^{next}_{bt}+\lambda U_{bt}\right],$$ where U is G at the next valid slot, or Vnext at the last valid slot. Numeric rewards and values share reward units; all other factors are dimensionless. Validity is a prefix so the recurrence never crosses absent data. Invalid outputs are zero. A fractional c changes future weight continuously; replacing it with a Boolean terminal flag loses information.

## Visual computation trace

| Reverse step | Inputs | Return |
|---|---|---|
| t1 | r2,Vnext20,c1,gamma.5 | 12 |
| t0 | r1,c.5,lambda1,nextG12 | 4 |

The table is the static visual and its text alternative; each row describes a transformation or decision.

## Worked calculation

rewards[[1,2]],next_values[[10,20]],continuation[[.5,1]],valid all,gamma .5, lam 1 => last 12, first 4.

## Why this matters on a robot

Errors in learned contact dynamics or termination predictions can compound through an imagined horizon. A numerically correct return remains conditional on those supplied predictions.

## Physical contract and limits

Latents and normalized actions are dimensionless. Rewards/values use a fixed caller-declared dimensionless reward scale; KL is measured in nats. Each ordered index is one fixed caller-declared control interval. Predicted continuation is a probability, not an elapsed duration. No implicit frame conversion. A bounded component with supplied tensors. Prediction loss inputs and deterministic imagined dynamics do not reproduce the complete trained recurrent stochastic world model, actor or benchmark.

Source: [primary paper](https://arxiv.org/html/2301.04104v2). Prerequisite: understand the observation/action schema supplied in the contract; no additional lesson is required.
