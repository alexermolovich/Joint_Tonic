---
schema_version: 1
paper_id: "2021-adversarial-motion-priors"
title: "AMP: Adversarial Motion Priors for Stylized Physics-Based Character Control"
authors: ["Peng, Xue Bin","Ma, Ze","Abbeel, Pieter","Levine, Sergey","Kanazawa, Angjoo"]
year: 2021
venue_or_status: "Author-deposited arXiv manuscript; final venue not asserted by this acquisition card."
primary_url: "https://arxiv.org/abs/2104.02180"
pdf_url: "https://arxiv.org/pdf/2104.02180"
local_pdf: "./2021-adversarial-motion-priors.pdf"
sha256: "93d9e8e40b3908d65e8b88ae3dcbe8d4cd69071d13f3234ad927462477472a29"
bytes: 8715012
pages: 20
topics: ["humanoid-dexterity-tactile","adversarial-motion-priors"]
modalities: ["proprioception","contacts","tactile","motion"]
track_role: "supporting"
open_access_status: "open-access-preprint"
redistribution_note: "Research copy only; verify the source license before redistribution."
execution_flow: {"title":"Core execution flow","description":"Follow the data through the mechanism. Training objectives and inference behavior are distinguished in the linked explanations.","nodes":[{"id":"stage-1","title":"Compare motion transitions","detail":"Train a discriminator on reference and policy-generated motion features.","column":0,"row":0,"section":"Compare motion transitions","problem_slugs":[],"planned_problems":["Construct Motion Discriminator Features"]},{"id":"stage-2","title":"Convert discrimination into style reward","detail":"Reward transitions resembling reference motion.","column":1,"row":0,"section":"Convert discrimination into style reward","problem_slugs":[],"planned_problems":["Compute an Adversarial Style Reward"]},{"id":"stage-3","title":"Learn task-directed behavior","detail":"Combine style and goal rewards through reinforcement learning.","column":2,"row":0,"section":"Learn task-directed behavior","problem_slugs":[],"planned_problems":["Balance Task and Style Objectives"]}],"edges":[{"from":"stage-1","to":"stage-2","label":"discriminator score"},{"from":"stage-2","to":"stage-3","label":"style reward"}]}
---

## Core paper explanation

Adversarial Motion Priors learns a motion-style reward from reference state transitions. A policy then combines that learned style with task rewards, without needing to track one fixed clip phase at every timestep.

## Execution flow

Follow the data through the mechanism. Training objectives and inference behavior are distinguished in the linked explanations.

### Compare motion transitions

For feature transitions $x=(\Phi(s),\Phi(s'))$, the least-squares discriminator core is
$$L_D=\mathbb E_{x\sim D_M}(D(x)-1)^2+\mathbb E_{x\sim D_\pi}(D(x)+1)^2.$$
$D_M$ is reference motion and $D_\pi$ policy experience. The paper also regularizes discriminator gradients. Features determine which aspects of style can be recognized.


**Planned exercise:** Construct Motion Discriminator Features.


### Convert discrimination into style reward

The bounded style reward is
$$r_{\mathrm{style}}(x)=\max(0,1-\tfrac14(D(x)-1)^2).$$
This follows the paper's least-squares formulation; substituting a sigmoid GAN reward changes the algorithm. A discriminator score is not a calibrated probability of physically safe motion.


**Planned exercise:** Compute an Adversarial Style Reward.


### Learn task-directed behavior

Use $r=w_sr_{\mathrm{style}}+w_gr_{\mathrm{goal}}$ with declared weights. The policy can compose behaviors from the motion distribution rather than following an explicit clip schedule. Evaluate both task success and motion quality; one can improve while the other degrades.


**Planned exercise:** Balance Task and Style Objectives.


## Implement the components

Exercises are attached to the corresponding execution stages and mathematical explanations above. Runnable links implement only their stated component scope. Planned titles are original authoring ideas, not reviewed contracts, runnable tasks, or claims of a reproduced paper. They enter the approved curriculum only through blueprint review.

- **Compare motion transitions:** Construct Motion Discriminator Features (planned).
- **Convert discrimination into style reward:** Compute an Adversarial Style Reward (planned).
- **Learn task-directed behavior:** Balance Task and Style Objectives (planned).

## Why this matters on a robot

Motion priors help produce coordinated locomotion or manipulation style. Reference-motion coverage and robot morphology constrain what transfers, and adversarial rewards can miss mechanically undesirable behavior outside their feature set.

## Sources and scope

[Primary paper](https://arxiv.org/abs/2104.02180) · [Open-access manuscript](https://arxiv.org/pdf/2104.02180)

This is an original explanation of selected mechanisms. Equations use the notation defined here; simplified teaching models are identified explicitly. Small component exercises do not reproduce the paper's full experiments. The local PDF is a research reference; its redistribution terms remain those recorded in the metadata.
