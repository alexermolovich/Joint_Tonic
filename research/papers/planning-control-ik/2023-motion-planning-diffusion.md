---
schema_version: 1
paper_id: "2023-motion-planning-diffusion"
title: "Motion Planning Diffusion: Learning and Planning of Robot Motions with Diffusion Models"
authors: ["Carvalho, Joao","Le, An T.","Baierl, Mark","Koert, Dorothea","Peters, Jan"]
year: 2023
venue_or_status: "Author-deposited arXiv manuscript; final venue not asserted by this acquisition card."
primary_url: "https://arxiv.org/abs/2308.01557"
pdf_url: "https://arxiv.org/pdf/2308.01557"
local_pdf: "./2023-motion-planning-diffusion.pdf"
sha256: "5045a1eef8b1e29e7007877083ddf26932fa6561717242e7a0b988cda751db95"
bytes: 2727520
pages: 9
topics: ["planning-control-ik","motion-planning-diffusion"]
modalities: ["joint-state","poses","obstacles","trajectories"]
track_role: "supporting"
open_access_status: "open-access-preprint"
redistribution_note: "Research copy only; verify the source license before redistribution."
execution_flow: {"title":"Core execution flow","description":"Follow the data through the mechanism. Training objectives and inference behavior are distinguished in the linked explanations.","nodes":[{"id":"stage-1","title":"Train a trajectory prior","detail":"Learn denoising from feasible motion examples.","column":0,"row":0,"section":"Train a trajectory prior","problem_slugs":["diffusion-action-noising"],"planned_problems":["Add Noise to a Joint-Space Path"]},{"id":"stage-2","title":"Guide toward low cost","detail":"Modify reverse sampling with differentiable planning objectives.","column":1,"row":0,"section":"Guide toward low cost","problem_slugs":[],"planned_problems":["Apply Collision-Cost Guidance During Denoising"]},{"id":"stage-3","title":"Check physical feasibility","detail":"Evaluate the generated motion independently of its likelihood.","column":2,"row":0,"section":"Check physical feasibility","problem_slugs":[],"planned_problems":["Check Endpoint and Smoothness Constraints"]}],"edges":[{"from":"stage-1","to":"stage-2","label":"learned prior"},{"from":"stage-2","to":"stage-3","label":"guided trajectories"}]}
---

## Core paper explanation

Motion Planning Diffusion learns a prior over robot trajectories and combines it with task and obstacle costs during denoising. The prior supplies plausible motion structure while guidance adapts samples to the current planning problem.

## Execution flow

Follow the data through the mechanism. Training objectives and inference behavior are distinguished in the linked explanations.

### Train a trajectory prior

For normalized trajectory $\tau\in\mathbb R^{H\times d}$,
$$\tau^k=\sqrt{\bar\alpha_k}\tau+\sqrt{1-\bar\alpha_k}\epsilon.$$
The training objective teaches recovery from noise. Joint order, timestep, endpoint conditioning, and any velocity channels must remain consistent across the dataset.


**Component practice**

- Supporting prerequisite: [Add Noise to an Action Sequence](/problems/diffusion-action-noising). Practices the stated data or mathematical operation; it does not implement this paper-specific stage in full.
- Add Noise to a Joint-Space Path — unreviewed idea; contract and evaluator required.

### Guide toward low cost

A probabilistic teaching view is
$$p(\tau\mid\mathrm{task})\propto p_\theta(\tau)\exp[-J(\tau)],$$
so the guidance contribution is $-\nabla_\tau J$. The cost can include collision clearance and endpoint conditions. Guidance scaling and denoising covariance affect the practical update; this density expression is not a claim of exact posterior sampling by finite steps.


**Component practice**

- Apply Collision-Cost Guidance During Denoising — unreviewed idea; contract and evaluator required.

### Check physical feasibility

Check limits and collision clearance over the interpolated path. A high prior likelihood does not prove feasibility in a new environment, and a small sampled collision cost can miss obstacles between waypoints. Compare planning success, smoothness, and compute under the same environment geometry.


**Component practice**

- Check Endpoint and Smoothness Constraints — unreviewed idea; contract and evaluator required.

## Implement the components

Each execution-flow node links the matching runnable component or names its planned problem. Planned titles are not runnable; labels distinguish reviewed drafts from unreviewed ideas.

- **Supporting prerequisite:** [Add Noise to an Action Sequence](/problems/diffusion-action-noising).

**Planned component problems:**

- Add Noise to a Joint-Space Path — unreviewed idea; contract and evaluator required.
- Apply Collision-Cost Guidance During Denoising — unreviewed idea; contract and evaluator required.
- Check Endpoint and Smoothness Constraints — unreviewed idea; contract and evaluator required.

These bounded exercises do not claim to reproduce the complete paper or its benchmark results.

## Why this matters on a robot

A learned prior can propose several motion modes around obstacles. Dataset coverage, cost gradients, and discretization resolution determine whether those modes remain useful in unfamiliar scenes.

## Sources and scope

[Primary paper](https://arxiv.org/abs/2308.01557) · [Open-access manuscript](https://arxiv.org/pdf/2308.01557)

This is an original explanation of selected mechanisms. Equations use the notation defined here; simplified teaching models are identified explicitly. Small component exercises do not reproduce the paper's full experiments. The local PDF is a research reference; its redistribution terms remain those recorded in the metadata.
