---
schema_version: 1
paper_id: "2024-dr-eureka"
title: "DrEureka: Language Model Guided Sim-To-Real Transfer"
authors: ["Ma, Yecheng Jason","Liang, William","Wang, Hung-Ju","Wang, Sam","Zhu, Yuke","Fan, Linxi","Bastani, Osbert","Jayaraman, Dinesh"]
year: 2024
venue_or_status: "Author-deposited arXiv manuscript; final venue not asserted by this acquisition card."
primary_url: "https://arxiv.org/abs/2406.01967"
pdf_url: "https://arxiv.org/pdf/2406.01967"
local_pdf: "./2024-dr-eureka.pdf"
sha256: "5931e0b03478694579daded847e39fb80115d5d9fa75cd250f059f691fb5f94c"
bytes: 34335250
pages: 28
topics: ["robot-learning-rl","dr-eureka"]
modalities: ["robot-state","rgb","actions","rewards"]
track_role: "supporting"
open_access_status: "open-access-preprint"
redistribution_note: "Research copy only; verify the source license before redistribution."
execution_flow: {"title":"Core execution flow","description":"Follow the data through the mechanism. Training objectives and inference behavior are distinguished in the linked explanations.","nodes":[{"id":"stage-1","title":"Design a transfer-oriented reward","detail":"Generate and evaluate rewards with explicit physical behavior requirements.","column":0,"row":0,"section":"Design a transfer-oriented reward","problem_slugs":[],"planned_problems":["Validate a Generated Reward Program"]},{"id":"stage-2","title":"Probe physics sensitivity","detail":"Evaluate the initial policy under perturbed simulator parameters.","column":1,"row":0,"section":"Probe physics sensitivity","problem_slugs":[],"planned_problems":["Compare Robustness Across Randomization Settings"]},{"id":"stage-3","title":"Train with generated randomization","detail":"Sample varied dynamics and validate physical transfer.","column":2,"row":0,"section":"Train with generated randomization","problem_slugs":["sample-dynamics-distributions"],"planned_problems":["Sample a Bounded Dynamics Randomization Config"]}],"edges":[{"from":"stage-1","to":"stage-2","label":"selected policy"},{"from":"stage-2","to":"stage-3","label":"randomization configuration"}]}
---

## Core paper explanation

DrEureka extends automated reward design with domain-randomization configuration for sim-to-real transfer. A learned policy is tested under perturbed physics to form reward-aware parameter priors before language-model-generated randomization distributions are used for training.

## Execution flow

Follow the data through the mechanism. Training objectives and inference behavior are distinguished in the linked explanations.

### Design a transfer-oriented reward

Candidate policies optimize $J(\pi;r)=\mathbb E[\sum_t\gamma^tr(s_t,a_t)]$. Reward instructions can discourage undesirable behavior, but a penalty is not a hard physical constraint. Preserve the independent success metric used to select candidates.


**Planned exercise:** Validate a Generated Reward Program.


### Probe physics sensitivity

For parameter setting $\theta$, estimate $S(\theta)=\mathbb E[\mathrm{success}\mid\pi,\theta]$. The resulting reward-aware physics priors inform plausible randomization ranges. A policy failing at a parameter value does not prove that value is physically impossible.


**Planned exercise:** Compare Robustness Across Randomization Settings.


### Train with generated randomization

The robust-training objective is $\mathbb E_{\theta\sim p_\psi(\theta),\tau\sim\pi,P_\theta}[R(\tau)]$. Distribution $p_\psi$ must preserve units, valid ranges, and parameter dependencies. Simulation evaluation selects configurations; real robot tests determine whether the chosen uncertainty model covers reality.


**Runnable component:** [Sample Mass, Friction, Delay, and Gain Distributions](/problems/sample-dynamics-distributions). Apply provided bounded parameter distributions; language-generated priors and real-robot transfer are separate tasks.

**Planned exercise:** Sample a Bounded Dynamics Randomization Config.


## Implement the components

Exercises are attached to the corresponding execution stages and mathematical explanations above. Runnable links implement only their stated component scope. Planned titles are original authoring ideas, not reviewed contracts, runnable tasks, or claims of a reproduced paper. They enter the approved curriculum only through blueprint review.

- **Design a transfer-oriented reward:** Validate a Generated Reward Program (planned).
- **Probe physics sensitivity:** Compare Robustness Across Randomization Settings (planned).
- **Train with generated randomization:** [Sample Mass, Friction, Delay, and Gain Distributions](/problems/sample-dynamics-distributions) (runnable component); Sample a Bounded Dynamics Randomization Config (planned).

## Why this matters on a robot

Automated randomization can reduce manual sim-to-real tuning. Independent parameter sampling can create implausible robots, while overly narrow ranges leave real dynamics uncovered.

## Sources and scope

[Primary paper](https://arxiv.org/abs/2406.01967) · [Open-access manuscript](https://arxiv.org/pdf/2406.01967)

This is an original explanation of selected mechanisms. Equations use the notation defined here; simplified teaching models are identified explicitly. Small component exercises do not reproduce the paper's full experiments. The local PDF is a research reference; its redistribution terms remain those recorded in the metadata.
