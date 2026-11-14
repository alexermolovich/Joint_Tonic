# Roll Out Imagined Latent Trajectories

## Intuition

Start imagination from one known latent state and propagate using actions and learned dynamics only. This small supplied model makes the information boundary visible without pretending to reproduce a full recurrent stochastic model.

## Mathematical mechanism

Let h have D latent coordinates, action a have A coordinates, and supplied parameter matrices W_h and W_a have shapes D by D and A by D. The original deterministic teaching block is $$h_{t+1}=\tanh(h_tW_h+a_tW_a+b),\quad r_t=h_{t+1}^Tw_r+b_r,\quad c_t=\sigma(h_{t+1}^Tw_c+b_c).$$ The sigmoid sigma maps its input to a probability. State output shape is B by (H+1) by D; reward and continuation shapes are B by H. Heads use the successor state. Low continuation does not stop dynamics evaluation; it weights later return calculations. There are no posterior observations, stochastic latent categories or actor updates inside this component.

## Visual computation trace

| Stage | Available information | Output |
|---|---|---|
| Initialize | supplied latent h0 | first state |
| Transition | current latent and supplied action | next latent |
| Heads | next latent only | reward and continuation |

The table is the static visual and its text alternative; each row describes a transformation or decision.

## Worked calculation

One state 0,action 0,all weights/biases0,H=1 -> states[[[0],[0]]],reward [[0]],continuation [[.5]].

## Why this matters on a robot

Errors in learned contact dynamics or termination predictions can compound through an imagined horizon. A numerically correct return remains conditional on those supplied predictions.

## Physical contract and limits

Latents and normalized actions are dimensionless. Rewards/values use a fixed caller-declared dimensionless reward scale; KL is measured in nats. Each ordered index is one fixed caller-declared control interval. Predicted continuation is a probability, not an elapsed duration. No implicit frame conversion. A bounded component with supplied tensors. Prediction loss inputs and deterministic imagined dynamics do not reproduce the complete trained recurrent stochastic world model, actor or benchmark.

Source: [primary paper](https://arxiv.org/html/2301.04104v2). Prerequisite: understand the observation/action schema supplied in the contract; no additional lesson is required.
