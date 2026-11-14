---
schema_version: 1
paper_id: "2018-learning-dexterous-manipulation"
title: "Learning Dexterous In-Hand Manipulation"
authors: ["OpenAI","Andrychowicz, Marcin","Baker, Bowen","Chociej, Maciek","Jozefowicz, Rafal","McGrew, Bob","Pachocki, Jakub","Petron, Arthur","Plappert, Matthias","Powell, Glenn","Ray, Alex","Schneider, Jonas","Sidor, Szymon","Tobin, Josh","Welinder, Peter","Weng, Lilian","Zaremba, Wojciech"]
year: 2018
venue_or_status: "Author-deposited arXiv manuscript; final venue not asserted by this acquisition card."
primary_url: "https://arxiv.org/abs/1808.00177"
pdf_url: "https://arxiv.org/pdf/1808.00177"
local_pdf: "./2018-learning-dexterous-manipulation.pdf"
sha256: "da6ec44dd0941d674ec58334ff630f83d7bd19e6062ab2837ccfa0b3b94f6f73"
bytes: 4590851
pages: 27
topics: ["humanoid-dexterity-tactile","learning-dexterous-manipulation"]
modalities: ["proprioception","contacts","tactile","motion"]
track_role: "supporting"
open_access_status: "open-access-preprint"
redistribution_note: "Research copy only; verify the source license before redistribution."
execution_flow: {"title":"Core execution flow","description":"Follow the data through the mechanism. Training objectives and inference behavior are distinguished in the linked explanations.","nodes":[{"id":"stage-1","title":"Randomize simulated experience","detail":"Vary dynamics, observations, and delays during training.","column":0,"row":0,"section":"Randomize simulated experience","problem_slugs":["sample-dynamics-distributions"],"planned_problems":["Sample Hand Dynamics Randomization"]},{"id":"stage-2","title":"Learn recurrent reorientation control","detail":"Use observation history to adapt behavior implicitly.","column":1,"row":0,"section":"Learn recurrent reorientation control","problem_slugs":[],"planned_problems":["Compute Object Rotation Tracking Error"]},{"id":"stage-3","title":"Deploy with measured observations","detail":"Combine visual object pose and hand sensing in the trained interface.","column":2,"row":0,"section":"Deploy with measured observations","problem_slugs":[],"planned_problems":["Evaluate Robustness to Sensor and Actuator Noise"]}],"edges":[{"from":"stage-1","to":"stage-2","label":"randomized rollouts"},{"from":"stage-2","to":"stage-3","label":"trained policy and pose estimator"}]}
---

## Core paper explanation

Learning Dexterous In-Hand Manipulation transfers a recurrent control policy from heavily randomized simulation to a real robotic hand. A separately trained visual pose estimator and measured hand information supply the policy observations.

## Execution flow

Follow the data through the mechanism. Training objectives and inference behavior are distinguished in the linked explanations.

### Randomize simulated experience

Training optimizes $\mathbb E_{\theta\sim p(\theta),\tau\sim\pi,P_\theta}[R(\tau)]$, where $\theta$ includes uncertain physical and sensing properties. Randomization ranges and correlations define the robustness target; arbitrary broad variation can make learning unnecessarily difficult.


**Runnable component:** [Sample Mass, Friction, Delay, and Gain Distributions](/problems/sample-dynamics-distributions). A bounded scalar-randomization primitive; the paper uses additional hand, appearance and observation distributions.

**Planned exercise:** Sample Hand Dynamics Randomization.


### Learn recurrent reorientation control

A recurrent controller updates $h_t=F(h_{t-1},o_t)$ and outputs $a_t\sim\pi(\cdot\mid h_t,o_t)$. For unit quaternions $q,q^*$, orientation error can be measured as
$$e_R=2\arccos(\min(1,|q^{*\top}q|)).$$
The absolute dot product handles the equivalent quaternion signs. Goal progress and dropping events shape the task reward.


**Planned exercise:** Compute Object Rotation Tracking Error.


### Deploy with measured observations

The paper trains vision separately on randomized rendered scenes. Real observations must preserve pose conventions, fingertip geometry, timing, and action scaling. Recurrent memory can support adaptation but does not explicitly identify every physical parameter.


**Planned exercise:** Evaluate Robustness to Sensor and Actuator Noise.


## Implement the components

Exercises are attached to the corresponding execution stages and mathematical explanations above. Runnable links implement only their stated component scope. Planned titles are original authoring ideas, not reviewed contracts, runnable tasks, or claims of a reproduced paper. They enter the approved curriculum only through blueprint review.

- **Randomize simulated experience:** [Sample Mass, Friction, Delay, and Gain Distributions](/problems/sample-dynamics-distributions) (runnable component); Sample Hand Dynamics Randomization (planned).
- **Learn recurrent reorientation control:** Compute Object Rotation Tracking Error (planned).
- **Deploy with measured observations:** Evaluate Robustness to Sensor and Actuator Noise (planned).

## Why this matters on a robot

Randomization and memory help tolerate modeling error in contact-rich dexterity. Unmodeled wear, sensor outages, or friction outside the training distribution can still cause object drops.

## Sources and scope

[Primary paper](https://arxiv.org/abs/1808.00177) · [Open-access manuscript](https://arxiv.org/pdf/1808.00177)

This is an original explanation of selected mechanisms. Equations use the notation defined here; simplified teaching models are identified explicitly. Small component exercises do not reproduce the paper's full experiments. The local PDF is a research reference; its redistribution terms remain those recorded in the metadata.
