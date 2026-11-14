---
schema_version: 1
paper_id: "2022-diffuser"
title: "Planning with Diffusion for Flexible Behavior Synthesis"
authors: ["Janner, Michael","Du, Yilun","Tenenbaum, Joshua B.","Levine, Sergey"]
year: 2022
venue_or_status: "Author-deposited arXiv manuscript; final venue not asserted by this acquisition card."
primary_url: "https://arxiv.org/abs/2205.09991"
pdf_url: "https://arxiv.org/pdf/2205.09991"
local_pdf: "./2022-diffuser.pdf"
sha256: "aafe149adb5476e8b8b061c02d26824c42fb14a71ce8ae37b1a0e375452d7a1f"
bytes: 10498721
pages: 14
topics: ["planning-control-ik","diffuser"]
modalities: ["joint-state","poses","obstacles","trajectories"]
track_role: "supporting"
open_access_status: "open-access-preprint"
redistribution_note: "Research copy only; verify the source license before redistribution."
execution_flow: {"title":"Core execution flow","description":"Follow the data through the mechanism. Training objectives and inference behavior are distinguished in the linked explanations.","nodes":[{"id":"stage-1","title":"Learn trajectory denoising","detail":"Corrupt and reconstruct complete state–action sequences.","column":0,"row":0,"section":"Learn trajectory denoising","problem_slugs":["diffusion-action-noising","diffusion-conditional-noise-loss"],"planned_problems":["Construct a State-Action Trajectory Tensor"]},{"id":"stage-2","title":"Condition the reverse process","detail":"Use endpoint inpainting and reward-based guidance.","column":1,"row":0,"section":"Condition the reverse process","problem_slugs":[],"planned_problems":["Clamp Goal Conditions During Denoising"]},{"id":"stage-3","title":"Execute and replan","detail":"Use the generated first action and update conditioning.","column":2,"row":0,"section":"Execute and replan","problem_slugs":["diffusion-receding-horizon-window"],"planned_problems":["Evaluate a Generated Plan Under Dynamics"]}],"edges":[{"from":"stage-1","to":"stage-2","label":"trajectory prior"},{"from":"stage-2","to":"stage-3","label":"planned trajectory"}]}
---

## Core paper explanation

Diffuser learns a distribution over whole state–action trajectories and uses denoising as a planning procedure. Goal conditioning and reward guidance modify samples while the learned trajectory prior supplies behavior structure.

## Execution flow

Follow the data through the mechanism. Training objectives and inference behavior are distinguished in the linked explanations.

### Learn trajectory denoising

Stack a trajectory as $\tau\in\mathbb R^{H\times(d_s+d_a)}$. Training noise is
$$\tau^k=\sqrt{\bar\alpha_k}\tau^0+\sqrt{1-\bar\alpha_k}\epsilon.$$
States and actions need separate normalization because their physical units differ. Denoising learns trajectory structure rather than only one-step dynamics.


**Component practice**

- Supporting prerequisite: [Add Noise to an Action Sequence](/problems/diffusion-action-noising). Practices the stated data or mathematical operation; it does not implement this paper-specific stage in full.
- Supporting prerequisite: [Compute a Conditional Noise-Prediction Loss](/problems/diffusion-conditional-noise-loss). Practices the stated data or mathematical operation; it does not implement this paper-specific stage in full.
- Construct a State-Action Trajectory Tensor — unreviewed idea; contract and evaluator required.

### Condition the reverse process

A guided reverse mean can be expressed schematically as
$$\mu' =\mu+\alpha\Sigma\nabla_\tau J(\mu),$$
where $J$ estimates trajectory return and $\alpha$ sets guidance strength. Fixed observed states or goals can be restored during denoising through inpainting. Reward guidance depends on a differentiable, meaningful gradient.


**Component practice**

- Clamp Goal Conditions During Denoising — unreviewed idea; contract and evaluator required.

### Execute and replan

After sampling, execute the first action, observe the real successor state, and plan again. A sampled future state is a model prediction, not a measured state. Check dynamics consistency and reward extrapolation, especially when guidance moves samples away from the training distribution.


**Component practice**

- Supporting prerequisite: [Execute a Receding-Horizon Action Window](/problems/diffusion-receding-horizon-window). Practices the stated data or mathematical operation; it does not implement this paper-specific stage in full.
- Evaluate a Generated Plan Under Dynamics — unreviewed idea; contract and evaluator required.

## Implement the components

Each execution-flow node links the matching runnable component or names its planned problem. Planned titles are not runnable; labels distinguish reviewed drafts from unreviewed ideas.

- **Supporting prerequisite:** [Add Noise to an Action Sequence](/problems/diffusion-action-noising).
- **Supporting prerequisite:** [Compute a Conditional Noise-Prediction Loss](/problems/diffusion-conditional-noise-loss).
- **Supporting prerequisite:** [Execute a Receding-Horizon Action Window](/problems/diffusion-receding-horizon-window).

**Planned component problems:**

- Construct a State-Action Trajectory Tensor — unreviewed idea; contract and evaluator required.
- Clamp Goal Conditions During Denoising — unreviewed idea; contract and evaluator required.
- Evaluate a Generated Plan Under Dynamics — unreviewed idea; contract and evaluator required.

These bounded exercises do not claim to reproduce the complete paper or its benchmark results.

## Why this matters on a robot

Trajectory priors can express multiple plausible plans. Strong reward guidance may exploit a learned return model or create physically inconsistent trajectories; rollout validation remains important.

## Sources and scope

[Primary paper](https://arxiv.org/abs/2205.09991) · [Open-access manuscript](https://arxiv.org/pdf/2205.09991)

This is an original explanation of selected mechanisms. Equations use the notation defined here; simplified teaching models are identified explicitly. Small component exercises do not reproduce the paper's full experiments. The local PDF is a research reference; its redistribution terms remain those recorded in the metadata.
