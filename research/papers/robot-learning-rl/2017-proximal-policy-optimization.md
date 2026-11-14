---
schema_version: 1
paper_id: "2017-proximal-policy-optimization"
title: "Proximal Policy Optimization Algorithms"
authors: ["Schulman, John","Wolski, Filip","Dhariwal, Prafulla","Radford, Alec","Klimov, Oleg"]
year: 2017
venue_or_status: "Author-deposited arXiv manuscript; final venue not asserted by this acquisition card."
primary_url: "https://arxiv.org/abs/1707.06347"
pdf_url: "https://arxiv.org/pdf/1707.06347"
local_pdf: "./2017-proximal-policy-optimization.pdf"
sha256: "e78feadadbdbb0b601b3c2bcc81404722cd431a489b307545f9b7bea1e8c4f5b"
bytes: 2923532
pages: 12
topics: ["robot-learning-rl","proximal-policy-optimization"]
modalities: ["robot-state","rgb","actions","rewards"]
track_role: "supporting"
open_access_status: "open-access-preprint"
redistribution_note: "Research copy only; verify the source license before redistribution."
execution_flow: {"title":"Core execution flow","description":"Follow the data through the mechanism. Training objectives and inference behavior are distinguished in the linked explanations.","nodes":[{"id":"stage-1","title":"Collect advantages and old probabilities","detail":"Freeze the behavior policy for a rollout batch.","column":0,"row":0,"section":"Collect advantages and old probabilities","problem_slugs":[],"planned_problems":["Normalize Batched Advantages"]},{"id":"stage-2","title":"Optimize the clipped surrogate","detail":"Limit the benefit of large policy-ratio changes.","column":1,"row":0,"section":"Optimize the clipped surrogate","problem_slugs":[],"planned_problems":["Compute the Clipped Policy Surrogate","Report Policy Update Clip Fractions"]},{"id":"stage-3","title":"Update value and collect again","detail":"Fit value targets, monitor policy change, and refresh experience.","column":2,"row":0,"section":"Update value and collect again","problem_slugs":[],"planned_problems":["Compute Value Targets Across Episode Boundaries"]}],"edges":[{"from":"stage-1","to":"stage-2","label":"rollout batch"},{"from":"stage-2","to":"stage-3","label":"updated policy"}]}
---

## Core paper explanation

PPO reuses a batch of on-policy experience for several optimization epochs while clipping the policy-ratio surrogate. The clipping discourages excessive improvement claims from large probability changes without imposing an exact trust-region constraint.

## Execution flow

Follow the data through the mechanism. Training objectives and inference behavior are distinguished in the linked explanations.

### Collect advantages and old probabilities

For action $a_t$, retain $\log\pi_{\mathrm{old}}(a_t\mid s_t)$ and advantage estimate $\hat A_t$. Returns and advantages must respect terminal versus time-limit boundaries. Old log probabilities are fixed targets during the update.


**Planned exercise:** Normalize Batched Advantages.


### Optimize the clipped surrogate

Define $r_t=\exp(\log\pi_\theta-\log\pi_{\mathrm{old}})$. Maximize
$$L^{\mathrm{clip}}=\mathbb E_t\min(r_t\hat A_t,\operatorname{clip}(r_t,1-\varepsilon,1+\varepsilon)\hat A_t).$$
The minimum handles positive and negative advantages differently. Clipping the ratio does not mean clipping gradients or guaranteeing a global KL bound.


**Planned exercise:** Compute the Clipped Policy Surrogate.

**Planned exercise:** Report Policy Update Clip Fractions.


### Update value and collect again

A value term commonly uses $(V_\theta(s_t)-\hat R_t)^2$, with entropy regularization encouraging exploration. Coefficients and any value clipping are implementation choices that must be declared. After bounded epochs, collect a new batch under the updated policy.


**Planned exercise:** Compute Value Targets Across Episode Boundaries.


## Implement the components

Exercises are attached to the corresponding execution stages and mathematical explanations above. Runnable links implement only their stated component scope. Planned titles are original authoring ideas, not reviewed contracts, runnable tasks, or claims of a reproduced paper. They enter the approved curriculum only through blueprint review.

- **Collect advantages and old probabilities:** Normalize Batched Advantages (planned).
- **Optimize the clipped surrogate:** Compute the Clipped Policy Surrogate (planned); Report Policy Update Clip Fractions (planned).
- **Update value and collect again:** Compute Value Targets Across Episode Boundaries (planned).

## Why this matters on a robot

PPO is convenient for parallel robot simulation. Stale data, incorrectly scaled continuous-action log probabilities, and reward exploitation can undermine training despite a well-behaved clipped loss.

## Sources and scope

[Primary paper](https://arxiv.org/abs/1707.06347) · [Open-access manuscript](https://arxiv.org/pdf/1707.06347)

This is an original explanation of selected mechanisms. Equations use the notation defined here; simplified teaching models are identified explicitly. Small component exercises do not reproduce the paper's full experiments. The local PDF is a research reference; its redistribution terms remain those recorded in the metadata.
