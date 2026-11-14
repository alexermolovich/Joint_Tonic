---
schema_version: 1
paper_id: "2021-rapid-motor-adaptation"
title: "RMA: Rapid Motor Adaptation for Legged Robots"
authors: ["Kumar, Ashish","Fu, Zipeng","Pathak, Deepak","Malik, Jitendra"]
year: 2021
venue_or_status: "Author-deposited arXiv manuscript; final venue not asserted by this acquisition card."
primary_url: "https://arxiv.org/abs/2107.04034"
pdf_url: "https://arxiv.org/pdf/2107.04034"
local_pdf: "./2021-rapid-motor-adaptation.pdf"
sha256: "d8660da881851756287efab24d85f5c629ba97878f70297eb429a8e8a9a57846"
bytes: 16534863
pages: 15
topics: ["humanoid-dexterity-tactile","rapid-motor-adaptation"]
modalities: ["proprioception","contacts","tactile","motion"]
track_role: "supporting"
open_access_status: "open-access-preprint"
redistribution_note: "Research copy only; verify the source license before redistribution."
execution_flow: {"title":"Core execution flow","description":"Follow the data through the mechanism. Training objectives and inference behavior are distinguished in the linked explanations.","nodes":[{"id":"stage-1","title":"Train with privileged extrinsics","detail":"Encode simulated environment factors for the base policy.","column":0,"row":0,"section":"Train with privileged extrinsics","problem_slugs":[],"planned_problems":["Build Privileged Dynamics-Latent Supervision"]},{"id":"stage-2","title":"Infer extrinsics from history","detail":"Train an adaptation module against the privileged latent.","column":1,"row":0,"section":"Infer extrinsics from history","problem_slugs":[],"planned_problems":["Window Proprioceptive History","Estimate a Latent Dynamics Context"]},{"id":"stage-3","title":"Run asynchronous adaptation","detail":"Use the latest inferred latent for high-rate control.","column":2,"row":0,"section":"Run asynchronous adaptation","problem_slugs":[],"planned_problems":["Track the Age of an Asynchronous Adaptation Latent","Evaluate Policy Recovery After a Parameter Change"]}],"edges":[{"from":"stage-1","to":"stage-2","label":"state-action history"},{"from":"stage-2","to":"stage-3","label":"adapted latent"}]}
---

## Core paper explanation

RMA learns a locomotion policy conditioned on a latent description of environmental factors, then trains an adaptation module to infer that latent from recent state/action history. Deployment uses the inferred latent rather than privileged simulator parameters.

## Execution flow

Follow the data through the mechanism. Training objectives and inference behavior are distinguished in the linked explanations.

### Train with privileged extrinsics

An environment encoder maps factors $e_t$ to $z_t=\mu(e_t)$. The base policy predicts $a_t=\pi(o_t,z_t)$. Factors can describe properties unavailable directly on the robot; their role is to teach useful adaptive behavior in simulation.


**Planned exercise:** Build Privileged Dynamics-Latent Supervision.


### Infer extrinsics from history

With history $h_t=(o_{t-H:t},a_{t-H:t-1})$, train
$$L_{\mathrm{adapt}}=\mathbb E\|\phi(h_t)-\mu(e_t)\|_2^2.$$
The target is a learned latent, not necessarily interpretable friction or mass. On-policy data helps align histories with the behavior encountered during deployment.


**Planned exercise:** Window Proprioceptive History.

**Planned exercise:** Estimate a Latent Dynamics Context.


### Run asynchronous adaptation

At deployment, $\hat z_t=\phi(h_t)$ replaces privileged $z_t$. The paper runs adaptation slower than the base controller, which consumes the most recent available latent. Timestamp the estimate; sudden changes can occur faster than the history window can identify them.


**Planned exercise:** Track the Age of an Asynchronous Adaptation Latent.

**Planned exercise:** Evaluate Policy Recovery After a Parameter Change.


## Implement the components

Exercises are attached to the corresponding execution stages and mathematical explanations above. Runnable links implement only their stated component scope. Planned titles are original authoring ideas, not reviewed contracts, runnable tasks, or claims of a reproduced paper. They enter the approved curriculum only through blueprint review.

- **Train with privileged extrinsics:** Build Privileged Dynamics-Latent Supervision (planned).
- **Infer extrinsics from history:** Window Proprioceptive History (planned); Estimate a Latent Dynamics Context (planned).
- **Run asynchronous adaptation:** Track the Age of an Asynchronous Adaptation Latent (planned); Evaluate Policy Recovery After a Parameter Change (planned).

## Why this matters on a robot

History-based adaptation can compensate for payload, terrain, and dynamics changes without retraining. Unobservable parameters, misleading contact histories, and stale adaptation estimates remain limits.

## Sources and scope

[Primary paper](https://arxiv.org/abs/2107.04034) · [Open-access manuscript](https://arxiv.org/pdf/2107.04034)

This is an original explanation of selected mechanisms. Equations use the notation defined here; simplified teaching models are identified explicitly. Small component exercises do not reproduce the paper's full experiments. The local PDF is a research reference; its redistribution terms remain those recorded in the metadata.
