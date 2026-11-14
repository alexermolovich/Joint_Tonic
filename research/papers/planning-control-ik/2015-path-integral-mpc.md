---
schema_version: 1
paper_id: "2015-path-integral-mpc"
title: "Model Predictive Path Integral Control using Covariance Variable Importance Sampling"
authors: ["Williams, Grady","Aldrich, Andrew","Theodorou, Evangelos"]
year: 2015
venue_or_status: "Author-deposited arXiv manuscript; final venue not asserted by this acquisition card."
primary_url: "https://arxiv.org/abs/1509.01149"
pdf_url: "https://arxiv.org/pdf/1509.01149"
local_pdf: "./2015-path-integral-mpc.pdf"
sha256: "f1e62491294b671689e908e2d1d4a9b738ea228ef5c545bd393f17f0b6636b6d"
bytes: 1023682
pages: 9
topics: ["planning-control-ik","path-integral-mpc"]
modalities: ["joint-state","poses","obstacles","trajectories"]
track_role: "supporting"
open_access_status: "open-access-preprint"
redistribution_note: "Research copy only; verify the source license before redistribution."
execution_flow: {"title":"Core execution flow","description":"Follow the data through the mechanism. Training objectives and inference behavior are distinguished in the linked explanations.","nodes":[{"id":"stage-1","title":"Sample control rollouts","detail":"Perturb a nominal sequence and simulate dynamics.","column":0,"row":0,"section":"Sample control rollouts","problem_slugs":[],"planned_problems":["Roll Out Perturbed Control Sequences"]},{"id":"stage-2","title":"Weight corrected costs","detail":"Use exponential weights with the required sampling correction.","column":1,"row":0,"section":"Weight corrected costs","problem_slugs":[],"planned_problems":["Normalize Exponential Trajectory Cost Weights"]},{"id":"stage-3","title":"Update and recede","detail":"Average useful perturbations and shift the horizon.","column":2,"row":0,"section":"Update and recede","problem_slugs":[],"planned_problems":["Update a Receding-Horizon Control Sequence"]}],"edges":[{"from":"stage-1","to":"stage-2","label":"rollout costs"},{"from":"stage-2","to":"stage-3","label":"normalized weights"}]}
---

## Core paper explanation

Model Predictive Path Integral control improves a nominal control sequence by evaluating many stochastic rollouts in parallel. Low-cost perturbations receive greater weight, and the controller executes only the first action before replanning.

## Execution flow

Follow the data through the mechanism. Training objectives and inference behavior are distinguished in the linked explanations.

### Sample control rollouts

For nominal controls $u_{0:H-1}$, sample noise $\epsilon_{k,t}$ and roll out $x_{t+1}=f(x_t,u_t+\epsilon_{k,t})$. Noise covariance, timestep, and control units must match the model. The paper's generalized importance sampling allows altered sampling drift and diffusion.


**Component practice**

- Roll Out Perturbed Control Sequences — unreviewed idea; contract and evaluator required.

### Weight corrected costs

For corrected rollout cost $S_k$ and temperature $\lambda>0$,
$$w_k=\frac{\exp(-(S_k-S_{\min})/\lambda)}{\sum_j\exp(-(S_j-S_{\min})/\lambda)}.$$
$S_k$ includes the path-integral control/importance terms, not only arbitrary state reward. Subtracting $S_{\min}$ stabilizes the exponential without changing normalized weights.


**Component practice**

- Normalize Exponential Trajectory Cost Weights — unreviewed idea; contract and evaluator required.

### Update and recede

The core update is
$$u_t\leftarrow u_t+\sum_k w_k\epsilon_{k,t}.$$
Execute the first control, observe the new state, and shift the plan. Clipping or changing the sampling distribution requires attention to the derivation; arbitrary modifications do not preserve every path-integral guarantee.


**Component practice**

- Update a Receding-Horizon Control Sequence — unreviewed idea; contract and evaluator required.

## Implement the components

Each execution-flow node links the matching runnable component or names its planned problem. Planned titles are not runnable; labels distinguish reviewed drafts from unreviewed ideas.


**Planned component problems:**

- Roll Out Perturbed Control Sequences — unreviewed idea; contract and evaluator required.
- Normalize Exponential Trajectory Cost Weights — unreviewed idea; contract and evaluator required.
- Update a Receding-Horizon Control Sequence — unreviewed idea; contract and evaluator required.

These bounded exercises do not claim to reproduce the complete paper or its benchmark results.

## Why this matters on a robot

MPPI handles nonlinear rollout models and parallel hardware well. Bad dynamics, weight collapse onto one sample, and delayed observations can yield poor control even with many rollouts.

## Sources and scope

[Primary paper](https://arxiv.org/abs/1509.01149) · [Open-access manuscript](https://arxiv.org/pdf/1509.01149)

This is an original explanation of selected mechanisms. Equations use the notation defined here; simplified teaching models are identified explicitly. Small component exercises do not reproduce the paper's full experiments. The local PDF is a research reference; its redistribution terms remain those recorded in the metadata.
