---
schema_version: 1
paper_id: 2021-robomimic
title: >-
  What Matters in Learning from Offline Human Demonstrations for Robot
  Manipulation
authors:
  - Ajay Mandlekar
  - Danfei Xu
  - Josiah Wong
  - Soroush Nasiriany
  - Chen Wang
  - Rohun Kulkarni
  - Li Fei-Fei
  - Silvio Savarese
  - Yuke Zhu
  - Roberto Martin-Martin
year: 2021
venue_or_status: CoRL 2021 (PMLR proceedings 2022)
primary_url: 'https://arxiv.org/abs/2108.03298'
pdf_url: 'https://arxiv.org/pdf/2108.03298'
local_pdf: ./2021-robomimic.pdf
sha256: 18283ff9cbb9645de4ccf32ca2de472f452e89761287e7ed578e3a1066bea5f1
bytes: 10782355
pages: 36
topics:
  - imitation-learning
  - offline-rl
  - robot-demonstrations
  - reproducibility
  - evaluation
modalities:
  - rgb
  - wrist-camera
  - proprioception
  - actions
  - trajectories
track_role: foundation
open_access_status: open-access-preprint
redistribution_note: Research copy only; verify the source license before redistribution.
execution_flow:
  title: Core execution flow
  description: >-
    Construct valid demonstration windows, train an offline policy, then
    evaluate closed-loop behavior across tasks and data-quality conditions.
  nodes:
    - id: stage-1
      title: Construct episode windows
      detail: >-
        Batch temporal data without crossing episode boundaries or leaking
        evaluation episodes.
      column: 0
      row: 0
      section: Construct episode windows
      problem_slugs:
        - act-sliding-action-chunks
        - validate-robot-episodes
        - scene-safe-trajectory-split
        - batch-variable-robot-episodes
      planned_problems: []
    - id: stage-2
      title: Fit an offline policy
      detail: >-
        Optimize a chosen imitation or offline-learning objective on fixed
        demonstrations.
      column: 1
      row: 0
      section: Fit an offline policy
      problem_slugs: []
      planned_problems:
        - Compute a Masked Behavior-Cloning Log-Likelihood
    - id: stage-3
      title: Select with rollout evidence
      detail: >-
        Measure actual task success and uncertainty on held-out evaluation
        conditions.
      column: 2
      row: 0
      section: Select with rollout evidence
      problem_slugs:
        - demonstration-quality-performance
        - validation-loss-rollout-ranking
        - offline-rollout-checkpoint-gate
      planned_problems: []
  edges:
    - from: stage-1
      to: stage-2
      label: demonstration batches
    - from: stage-2
      to: stage-3
      label: candidate policies
---

## Core paper explanation

robomimic studies offline robot learning from human demonstrations of different quality and provides reproducible data and learning tools. Its experiments show that dataset composition, observation/action interfaces, temporal modeling, and policy selection materially affect success. A low supervised loss does not necessarily identify the policy that performs best when its own actions change future observations.

## Execution flow

Construct valid demonstration windows, train an offline policy, then evaluate closed-loop behavior across tasks and data-quality conditions.

### Construct episode windows

For episode length $T$ and window horizon $H$, a valid unpadded start satisfies $0\le t\le T-H$. A padded window uses mask

$$
M_k=\mathbf1[t+k<T],\qquad k=0,\ldots,H-1.
$$

Keep observation/action alignment and source episode identity. [Robot episode validation](/problems/validate-robot-episodes) checks related shape, value, and timing contracts before windowing.


**Component practice**

- Supporting prerequisite: [Build Sliding Action Chunks with Padding Masks](/problems/act-sliding-action-chunks). Practices the stated data or mathematical operation; it does not implement this paper-specific stage in full.
- Supporting prerequisite: [Validate a Multimodal Robot Episode Schema](/problems/validate-robot-episodes). Practices the stated data or mathematical operation; it does not implement this paper-specific stage in full.
- Runnable component: [Split Robot Trajectories Without Scene Leakage](/problems/scene-safe-trajectory-split). Uses the bounded contract; no full paper reproduction is claimed.
- Runnable component: [Batch Variable-Length Episodes with Masks](/problems/batch-variable-robot-episodes). Uses the bounded contract; no full paper reproduction is claimed.


### Fit an offline policy

For behavior cloning with policy density $\pi_\theta(a\mid o)$,

$$
\mathcal L_{\mathrm{BC}}=-\mathbb E_{(o,a)\sim D}\log\pi_\theta(a\mid o).
$$

The paper evaluates several algorithms; this is one important baseline, not a formula for all of them. A recurrent policy conditions on history and must reset hidden state at episode boundaries. Demonstration quality and coverage change the meaning of the offline objective.


**Component practice**

- Compute a Masked Behavior-Cloning Log-Likelihood — unreviewed idea; contract and evaluator required.


### Select with rollout evidence

For $N$ evaluation episodes with success indicators $s_i$,

$$
\hat p=\frac1N\sum_i s_i.
$$

Report episode count and uncertainty, and compare across seeds and task slices. Checkpoint selection using training loss alone may favor a policy with worse closed-loop behavior. Reusing the evaluation set repeatedly for tuning also changes the interpretation of held-out results.


**Component practice**

- Runnable component: [Report Performance by Demonstration Quality](/problems/demonstration-quality-performance). Uses the bounded contract; no full paper reproduction is claimed.
- Runnable component: [Compare Validation Loss with Rollout Success](/problems/validation-loss-rollout-ranking). Uses the bounded contract; no full paper reproduction is claimed.
- Runnable component: [Select a Checkpoint with Offline and Rollout Gates](/problems/offline-rollout-checkpoint-gate). Uses the bounded contract; no full paper reproduction is claimed.


## Implement the components

Runnable components and supporting prerequisites are attached to their matching execution-flow stages. Remaining titles are planned ideas requiring implementation and review.

- **Supporting prerequisite:** [Build Sliding Action Chunks with Padding Masks](/problems/act-sliding-action-chunks).
- **Supporting prerequisite:** [Validate a Multimodal Robot Episode Schema](/problems/validate-robot-episodes).
- **Runnable component:** [Split Robot Trajectories Without Scene Leakage](/problems/scene-safe-trajectory-split).

**Planned component problems:**

- Runnable component: [Batch Variable-Length Episodes with Masks](/problems/batch-variable-robot-episodes). Uses the bounded contract; no full paper reproduction is claimed.
- Compute a Masked Behavior-Cloning Log-Likelihood — unreviewed idea; contract and evaluator required.
- Runnable component: [Report Performance by Demonstration Quality](/problems/demonstration-quality-performance). Uses the bounded contract; no full paper reproduction is claimed.
- Runnable component: [Compare Validation Loss with Rollout Success](/problems/validation-loss-rollout-ranking). Uses the bounded contract; no full paper reproduction is claimed.
- Runnable component: [Select a Checkpoint with Offline and Rollout Gates](/problems/offline-rollout-checkpoint-gate). Uses the bounded contract; no full paper reproduction is claimed.

These exercises implement their stated contracts, not a complete paper reproduction.


## Why this matters on a robot

Human demonstrations contain pauses, corrections, varied skill, and incomplete coverage. A learned policy will visit states not present in the dataset. Preserve dataset provenance and evaluate recovery from deviations, not only reproduction of successful demonstration actions.

## Sources and scope

[Primary paper](https://arxiv.org/abs/2108.03298) · [Open-access manuscript](https://arxiv.org/pdf/2108.03298)

This is an original explanation of selected mechanisms. Equations use the notation defined here; simplified teaching models are identified explicitly. Small component exercises do not reproduce the paper's full experiments. The local PDF is a research reference; its redistribution terms remain those recorded in the metadata.
