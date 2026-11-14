---
schema_version: 1
paper_id: 2023-eureka
title: 'Eureka: Human-Level Reward Design via Coding Large Language Models'
authors:
  - 'Ma, Yecheng Jason'
  - 'Liang, William'
  - 'Wang, Guanzhi'
  - 'Huang, De-An'
  - 'Bastani, Osbert'
  - 'Jayaraman, Dinesh'
  - 'Zhu, Yuke'
  - 'Fan, Linxi'
  - 'Anandkumar, Anima'
year: 2023
venue_or_status: >-
  Author-deposited arXiv manuscript; final venue not asserted by this
  acquisition card.
primary_url: 'https://arxiv.org/abs/2310.12931'
pdf_url: 'https://arxiv.org/pdf/2310.12931'
local_pdf: ./2023-eureka.pdf
sha256: aa3b6350a92e4e8b1d894d0879d0af72df2fe76b3fe5d9341151924cb5884f74
bytes: 3896844
pages: 45
topics:
  - robot-learning-rl
  - eureka
modalities:
  - robot-state
  - rgb
  - actions
  - rewards
track_role: supporting
open_access_status: open-access-preprint
redistribution_note: Research copy only; verify the source license before redistribution.
execution_flow:
  title: Core execution flow
  description: >-
    Follow the data through the mechanism. Training objectives and inference
    behavior are distinguished in the linked explanations.
  nodes:
    - id: stage-1
      title: Generate reward candidates
      detail: Use task description and environment code to propose executable rewards.
      column: 0
      row: 0
      section: Generate reward candidates
      problem_slugs:
        - eureka-reward-output-contract
      planned_problems: []
    - id: stage-2
      title: Train and evaluate policies
      detail: Optimize each reward and score behavior with an independent task metric.
      column: 1
      row: 0
      section: Train and evaluate policies
      problem_slugs:
        - validation-loss-rollout-ranking
        - eureka-rank-rollout-candidates
      planned_problems: []
    - id: stage-3
      title: Reflect and revise
      detail: >-
        Use learning curves and reward-component statistics to improve
        candidates.
      column: 2
      row: 0
      section: Reflect and revise
      problem_slugs:
        - eureka-reward-component-diagnostics
      planned_problems: []
  edges:
    - from: stage-1
      to: stage-2
      label: reward programs
    - from: stage-2
      to: stage-3
      label: training diagnostics
---

## Core paper explanation

Eureka uses a language model to generate reward programs, trains policies with those rewards, and feeds performance diagnostics back into reward revision. The language model designs a learning signal; reinforcement learning still produces the motor policy.

## Execution flow

Follow the data through the mechanism. Training objectives and inference behavior are distinguished in the linked explanations.

### Generate reward candidates

A candidate reward is a program $r_k(s,a,s')$. It must use available state variables and return finite values with the expected batch shape. Executability and sensible scaling are prerequisites, not evidence that the reward expresses the intended task.


**Implement this component:** [Validate a Reward Function Contract](/problems/eureka-reward-output-contract).


### Train and evaluate policies

A useful distinction is between the reward used to train a policy and the independent metric used to select it. Let candidate k provide reward $r_k$, state $s_t$, action $a_t$, next state $s_{t+1}$, and dimensionless discount $0\le\gamma<1$. A finite-horizon teaching formulation is

$$
J_k(\pi)=\mathbb E_{\tau\sim\pi}\!\left[\sum_{t=0}^{H-1}\gamma^t r_k(s_t,a_t,s_{t+1})\right],\qquad
\pi_k\approx\arg\max_\pi J_k(\pi).
$$

Here H counts environment steps and trajectory tau contains states/actions collected under that policy. For N independent evaluation trials with binary task outcomes $y_{kn}$, use a separate score

$$
\widehat M_k=\frac1N\sum_{n=1}^{N}y_{kn}.
$$

This is an explanatory decomposition of reward search, not a claim of exact inner optimization or a specific statistical selection rule in the paper. Candidate A might accumulate shaped return100 but succeed in2/5 trials; candidate B might return10 and succeed in4/5. The independent rates0.4 versus0.8 favor B despite its smaller reward scale. [Compare Validation Loss with Rollout Success](/problems/validation-loss-rollout-ranking) is a related runnable diagnostic of surrogate-versus-behavior ranking, not an implementation of Eureka's reward-code generation.

| Candidate | Training signal | Independent task success | Interpretation |
|---|---|---|---|
| A | larger return | 2/5 | reward may be easy to exploit |
| B | smaller return | 4/5 | better measured task behavior |

The table is a static text alternative to the selection flow; no animation is needed.


The inner loop learns $\pi_k\approx\arg\max_\pi\mathbb E[\sum_t\gamma^tr_k]$. The outer loop compares $M(\pi_k)$ using a task metric $M$, which should remain independent of reward scale. This bilevel view explains the method without claiming exact optimization.


**Implement this component:** [Rank Reward Candidates by Rollout Evidence](/problems/eureka-rank-rollout-candidates).


### Reflect and revise

Feedback includes which terms activate, saturate, or fail to correlate with success. Keep reward code, prompts, simulator version, seeds, and evaluation outcomes together. A larger shaped reward alone is not proof of a better policy.


**Implement this component:** [Aggregate Reward-Component Diagnostics](/problems/eureka-reward-component-diagnostics).


## Implement the components

Exercises are attached to the corresponding execution stages and mathematical explanations above. Runnable links implement only their stated component scope. Planned titles are original authoring ideas, not reviewed contracts, runnable tasks, or claims of a reproduced paper. They enter the approved curriculum only through blueprint review.

- **Generate reward candidates:** [Validate a Reward Function Contract](/problems/eureka-reward-output-contract).
- **Train and evaluate policies:** [Rank Reward Candidates by Rollout Evidence](/problems/eureka-rank-rollout-candidates).
- **Reflect and revise:** [Aggregate Reward-Component Diagnostics](/problems/eureka-reward-component-diagnostics).

## Why this matters on a robot

Automated reward design can explore useful shaping faster. Generated rewards may exploit simulator shortcuts or reward unsafe motion; independent task evaluation and physical constraints remain essential.

## Sources and scope

[Primary paper](https://arxiv.org/abs/2310.12931) · [Open-access manuscript](https://arxiv.org/pdf/2310.12931)

This is an original explanation of selected mechanisms. Equations use the notation defined here; simplified teaching models are identified explicitly. Small component exercises do not reproduce the paper's full experiments. The local PDF is a research reference; its redistribution terms remain those recorded in the metadata.
