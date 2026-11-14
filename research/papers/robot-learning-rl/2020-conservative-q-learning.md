---
schema_version: 1
paper_id: "2020-conservative-q-learning"
title: "Conservative Q-Learning for Offline Reinforcement Learning"
authors: ["Kumar, Aviral","Zhou, Aurick","Tucker, George","Levine, Sergey"]
year: 2020
venue_or_status: "Author-deposited arXiv manuscript; final venue not asserted by this acquisition card."
primary_url: "https://arxiv.org/abs/2006.04779"
pdf_url: "https://arxiv.org/pdf/2006.04779"
local_pdf: "./2020-conservative-q-learning.pdf"
sha256: "2bae51a0b45635ab714df39446cd656a9f4f1c503f512d6d0ce1eec3198d1716"
bytes: 1632504
pages: 31
topics: ["robot-learning-rl","conservative-q-learning"]
modalities: ["robot-state","rgb","actions","rewards"]
track_role: "supporting"
open_access_status: "open-access-preprint"
redistribution_note: "Research copy only; verify the source license before redistribution."
execution_flow: {"title":"Core execution flow","description":"Follow the data through the mechanism. Training objectives and inference behavior are distinguished in the linked explanations.","nodes":[{"id":"stage-1","title":"Fit logged transitions","detail":"Construct Bellman targets from a fixed dataset.","column":0,"row":0,"section":"Fit logged transitions","problem_slugs":[],"planned_problems":["Construct Offline Bellman Targets with Termination Masks"]},{"id":"stage-2","title":"Penalize unsupported values","detail":"Lower broad action values relative to dataset actions.","column":1,"row":0,"section":"Penalize unsupported values","problem_slugs":[],"planned_problems":["Compute a Conservative Q Penalty","Compare Logged and Sampled Action Values"]},{"id":"stage-3","title":"Extract and evaluate a policy","detail":"Improve behavior while checking conservatism and coverage.","column":2,"row":0,"section":"Extract and evaluate a policy","problem_slugs":[],"planned_problems":["Evaluate Offline Policy Support"]}],"edges":[{"from":"stage-1","to":"stage-2","label":"critic predictions"},{"from":"stage-2","to":"stage-3","label":"regularized critic"}]}
---

## Core paper explanation

CQL addresses offline reinforcement learning by penalizing overoptimistic action values outside the logged behavior distribution. It couples Bellman fitting with a conservative regularizer rather than assuming arbitrary critic-selected actions are supported by data.

## Execution flow

Follow the data through the mechanism. Training objectives and inference behavior are distinguished in the linked explanations.

### Fit logged transitions

For dataset $D$, the ordinary critic term is $L_{\mathrm{TD}}=\mathbb E_D[(Q(s,a)-y)^2]$. Offline training cannot collect new transitions to correct every mistaken high-value prediction, making unsupported actions especially problematic.


**Planned exercise:** Construct Offline Bellman Targets with Termination Masks.


### Penalize unsupported values

A discrete-action CQL form is
$$L=L_{\mathrm{TD}}+\alpha\mathbb E_s\left[\log\sum_a e^{Q(s,a)}-\mathbb E_{a\sim D(\cdot\mid s)}Q(s,a)\right].$$
Continuous-action implementations approximate the action integral using sampled proposals and appropriate density corrections; directly summing a few arbitrary actions is not identical.


**Planned exercise:** Compute a Conservative Q Penalty.

**Planned exercise:** Compare Logged and Sampled Action Values.


### Extract and evaluate a policy

Larger $\alpha$ strengthens the conservative pressure but can also suppress useful actions. Theoretical lower-bound results depend on the stated assumptions; the regularizer is not an unconditional safety certificate. Evaluate offline selection separately from real rollout success.


**Planned exercise:** Evaluate Offline Policy Support.


## Implement the components

Exercises are attached to the corresponding execution stages and mathematical explanations above. Runnable links implement only their stated component scope. Planned titles are original authoring ideas, not reviewed contracts, runnable tasks, or claims of a reproduced paper. They enter the approved curriculum only through blueprint review.

- **Fit logged transitions:** Construct Offline Bellman Targets with Termination Masks (planned).
- **Penalize unsupported values:** Compute a Conservative Q Penalty (planned); Compare Logged and Sampled Action Values (planned).
- **Extract and evaluate a policy:** Evaluate Offline Policy Support (planned).

## Why this matters on a robot

Conservative values help reuse logged robot experience without unrestricted exploration. Dataset gaps and biased reward labels remain limits; excessive conservatism can keep a policy from improving beyond weak demonstrations.

## Sources and scope

[Primary paper](https://arxiv.org/abs/2006.04779) · [Open-access manuscript](https://arxiv.org/pdf/2006.04779)

This is an original explanation of selected mechanisms. Equations use the notation defined here; simplified teaching models are identified explicitly. Small component exercises do not reproduce the paper's full experiments. The local PDF is a research reference; its redistribution terms remain those recorded in the metadata.
