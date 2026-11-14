---
schema_version: 1
paper_id: "2023-eureka"
title: "Eureka: Human-Level Reward Design via Coding Large Language Models"
authors: ["Ma, Yecheng Jason","Liang, William","Wang, Guanzhi","Huang, De-An","Bastani, Osbert","Jayaraman, Dinesh","Zhu, Yuke","Fan, Linxi","Anandkumar, Anima"]
year: 2023
venue_or_status: "Author-deposited arXiv manuscript; final venue not asserted by this acquisition card."
primary_url: "https://arxiv.org/abs/2310.12931"
pdf_url: "https://arxiv.org/pdf/2310.12931"
local_pdf: "./2023-eureka.pdf"
sha256: "aa3b6350a92e4e8b1d894d0879d0af72df2fe76b3fe5d9341151924cb5884f74"
bytes: 3896844
pages: 45
topics: ["robot-learning-rl","eureka"]
modalities: ["robot-state","rgb","actions","rewards"]
track_role: "supporting"
open_access_status: "open-access-preprint"
redistribution_note: "Research copy only; verify the source license before redistribution."
execution_flow: {"title":"Core execution flow","description":"Follow the data through the mechanism. Training objectives and inference behavior are distinguished in the linked explanations.","nodes":[{"id":"stage-1","title":"Generate reward candidates","detail":"Use task description and environment code to propose executable rewards.","column":0,"row":0,"section":"Generate reward candidates","problem_slugs":[],"planned_problems":["Validate a Reward Function Contract"]},{"id":"stage-2","title":"Train and evaluate policies","detail":"Optimize each reward and score behavior with an independent task metric.","column":1,"row":0,"section":"Train and evaluate policies","problem_slugs":[],"planned_problems":["Rank Reward Candidates by Rollout Evidence"]},{"id":"stage-3","title":"Reflect and revise","detail":"Use learning curves and reward-component statistics to improve candidates.","column":2,"row":0,"section":"Reflect and revise","problem_slugs":[],"planned_problems":["Aggregate Reward-Component Diagnostics"]}],"edges":[{"from":"stage-1","to":"stage-2","label":"reward programs"},{"from":"stage-2","to":"stage-3","label":"training diagnostics"}]}
---

## Core paper explanation

Eureka uses a language model to generate reward programs, trains policies with those rewards, and feeds performance diagnostics back into reward revision. The language model designs a learning signal; reinforcement learning still produces the motor policy.

## Execution flow

Follow the data through the mechanism. Training objectives and inference behavior are distinguished in the linked explanations.

### Generate reward candidates

A candidate reward is a program $r_k(s,a,s')$. It must use available state variables and return finite values with the expected batch shape. Executability and sensible scaling are prerequisites, not evidence that the reward expresses the intended task.


**Planned exercise:** Validate a Reward Function Contract.


### Train and evaluate policies

The inner loop learns $\pi_k\approx\arg\max_\pi\mathbb E[\sum_t\gamma^tr_k]$. The outer loop compares $M(\pi_k)$ using a task metric $M$, which should remain independent of reward scale. This bilevel view explains the method without claiming exact optimization.


**Planned exercise:** Rank Reward Candidates by Rollout Evidence.


### Reflect and revise

Feedback includes which terms activate, saturate, or fail to correlate with success. Keep reward code, prompts, simulator version, seeds, and evaluation outcomes together. A larger shaped reward alone is not proof of a better policy.


**Planned exercise:** Aggregate Reward-Component Diagnostics.


## Implement the components

Exercises are attached to the corresponding execution stages and mathematical explanations above. Runnable links implement only their stated component scope. Planned titles are original authoring ideas, not reviewed contracts, runnable tasks, or claims of a reproduced paper. They enter the approved curriculum only through blueprint review.

- **Generate reward candidates:** Validate a Reward Function Contract (planned).
- **Train and evaluate policies:** Rank Reward Candidates by Rollout Evidence (planned).
- **Reflect and revise:** Aggregate Reward-Component Diagnostics (planned).

## Why this matters on a robot

Automated reward design can explore useful shaping faster. Generated rewards may exploit simulator shortcuts or reward unsafe motion; independent task evaluation and physical constraints remain essential.

## Sources and scope

[Primary paper](https://arxiv.org/abs/2310.12931) · [Open-access manuscript](https://arxiv.org/pdf/2310.12931)

This is an original explanation of selected mechanisms. Equations use the notation defined here; simplified teaching models are identified explicitly. Small component exercises do not reproduce the paper's full experiments. The local PDF is a research reference; its redistribution terms remain those recorded in the metadata.
