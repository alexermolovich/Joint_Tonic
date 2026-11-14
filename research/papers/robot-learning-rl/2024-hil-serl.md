---
schema_version: 1
paper_id: "2024-hil-serl"
title: "Precise and Dexterous Robotic Manipulation via Human-in-the-Loop Reinforcement Learning"
authors: ["Luo, Jianlan","Xu, Charles","Wu, Jeffrey","Levine, Sergey"]
year: 2024
venue_or_status: "Author-deposited arXiv manuscript; final venue not asserted by this acquisition card."
primary_url: "https://arxiv.org/abs/2410.21845"
pdf_url: "https://arxiv.org/pdf/2410.21845"
local_pdf: "./2024-hil-serl.pdf"
sha256: "547a4d5d9440a3f70a773798813db1c8a612f006a6994398bbee2a566daab526"
bytes: 23020066
pages: 54
topics: ["robot-learning-rl","hil-serl"]
modalities: ["robot-state","rgb","actions","rewards"]
track_role: "supporting"
open_access_status: "open-access-preprint"
redistribution_note: "Research copy only; verify the source license before redistribution."
execution_flow: {"title":"Core execution flow","description":"Follow the data through the mechanism. Training objectives and inference behavior are distinguished in the linked explanations.","nodes":[{"id":"stage-1","title":"Collect policy and corrective actions","detail":"Let a human temporarily take control when behavior needs correction.","column":0,"row":0,"section":"Collect policy and corrective actions","problem_slugs":[],"planned_problems":["Label Human Intervention Segments"]},{"id":"stage-2","title":"Learn from mixed replay","detail":"Combine demonstration/correction evidence with online experience.","column":1,"row":0,"section":"Learn from mixed replay","problem_slugs":[],"planned_problems":["Mix Intervention and Autonomous Replay"]},{"id":"stage-3","title":"Update and evaluate autonomy","detail":"Distribute new policies and track success without assistance.","column":2,"row":0,"section":"Update and evaluate autonomy","problem_slugs":[],"planned_problems":["Gate an Online Policy Update"]}],"edges":[{"from":"stage-1","to":"stage-2","label":"labeled transitions"},{"from":"stage-2","to":"stage-3","label":"learner updates"}]}
---

## Core paper explanation

HIL-SERL combines real-robot off-policy reinforcement learning with human demonstrations and online corrective interventions. An actor, learner, replay storage, and learned success rewards form an integrated training system.

## Execution flow

Follow the data through the mechanism. Training objectives and inference behavior are distinguished in the linked explanations.

### Collect policy and corrective actions

Record executed action $a_t$ and source label $h_t\in\{\mathrm{policy},\mathrm{human}\}$. When a human intervenes, the replay transition must contain the action actually sent to the controller, not the policy proposal that was overridden.


**Planned exercise:** Label Human Intervention Segments.


### Learn from mixed replay

A teaching replay mixture is $D_{\mathrm{batch}}\sim\eta D_{\mathrm{demo}}+(1-\eta)D_{\mathrm{online}}$. The actual system's buffer composition and sampling schedule must be retained. Critic targets use $y=r+\gamma(1-d)V_{\mathrm{target}}(s')$ under the chosen off-policy algorithm.


**Planned exercise:** Mix Intervention and Autonomous Replay.


### Update and evaluate autonomy

A success classifier supplies task reward from observations. Classifier false positives can be exploited by the policy. Report autonomous success separately from training success with interventions, together with human time, interaction budget, and policy version.


**Planned exercise:** Gate an Online Policy Update.


## Implement the components

Exercises are attached to the corresponding execution stages and mathematical explanations above. Runnable links implement only their stated component scope. Planned titles are original authoring ideas, not reviewed contracts, runnable tasks, or claims of a reproduced paper. They enter the approved curriculum only through blueprint review.

- **Collect policy and corrective actions:** Label Human Intervention Segments (planned).
- **Learn from mixed replay:** Mix Intervention and Autonomous Replay (planned).
- **Update and evaluate autonomy:** Gate an Online Policy Update (planned).

## Why this matters on a robot

Corrections can focus expensive experience on useful recovery behavior. Hidden human assistance or incorrect action-source logging can make a policy appear more autonomous than it is.

## Sources and scope

[Primary paper](https://arxiv.org/abs/2410.21845) · [Open-access manuscript](https://arxiv.org/pdf/2410.21845)

This is an original explanation of selected mechanisms. Equations use the notation defined here; simplified teaching models are identified explicitly. Small component exercises do not reproduce the paper's full experiments. The local PDF is a research reference; its redistribution terms remain those recorded in the metadata.
