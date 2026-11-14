---
schema_version: 1
paper_id: 2023-bridgedata-v2
title: 'BridgeData V2: A Dataset for Robot Learning at Scale'
authors:
  - 'Walke, Homer'
  - 'Black, Kevin'
  - 'Lee, Abraham'
  - 'Kim, Moo Jin'
  - 'Du, Max'
  - 'Zheng, Chongyi'
  - 'Zhao, Tony'
  - 'Hansen-Estruch, Philippe'
  - 'Vuong, Quan'
  - 'He, Andre'
  - 'Myers, Vivek'
  - 'Fang, Kuan'
  - 'Finn, Chelsea'
  - 'Levine, Sergey'
year: 2023
venue_or_status: >-
  Author-deposited arXiv manuscript; final venue not asserted by this
  acquisition card.
primary_url: 'https://arxiv.org/abs/2308.12952'
pdf_url: 'https://arxiv.org/pdf/2308.12952'
local_pdf: ./2023-bridgedata-v2.pdf
sha256: aa5fdac48bf9122b22f88150d45575cb0685f2a2f761ca6fc570be743022819b
bytes: 3258884
pages: 15
topics:
  - mlops-data-deployment
  - bridgedata-v2
modalities:
  - datasets
  - model-artifacts
  - logs
  - metrics
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
      title: Normalize episode interfaces
      detail: >-
        Keep observations, actions, instructions, and environment identity
        together.
      column: 0
      row: 0
      section: Normalize episode interfaces
      problem_slugs:
        - validate-robot-episodes
      planned_problems:
        - Normalize Multi-Environment Robot Records
    - id: stage-2
      title: Train conditioned behavior
      detail: Use language or visual goals as task context.
      column: 1
      row: 0
      section: Train conditioned behavior
      problem_slugs:
        - balance-multidataset-batch
      planned_problems: []
    - id: stage-3
      title: Test generalization
      detail: 'Hold out task, environment, or object conditions deliberately.'
      column: 2
      row: 0
      section: Test generalization
      problem_slugs: []
      planned_problems:
        - Evaluate Transfer by Environment Slice
  edges:
    - from: stage-1
      to: stage-2
      label: curated trajectories
    - from: stage-2
      to: stage-3
      label: trained policies
---

## Core paper explanation

BridgeData V2 collects diverse manipulation experience across tasks and environments with a common accessible robot platform. It supports goal-image and language-conditioned learning and evaluates several imitation and offline-RL methods.

## Execution flow

Follow the data through the mechanism. Training objectives and inference behavior are distinguished in the linked explanations.

### Normalize episode interfaces

For action channel $j$, a teaching normalization is $\tilde a_j=(a_j-\mu_j)/s_j$ with $s_j>0$. Statistics must be fitted only on the declared training split and stored with the model. Normalization does not erase differences in control mode or camera setup.


**Component practice**

- Supporting prerequisite: [Validate a Multimodal Robot Episode Schema](/problems/validate-robot-episodes). Practices the stated data or mathematical operation; it does not implement this paper-specific stage in full.
- Normalize Multi-Environment Robot Records — unreviewed idea; contract and evaluator required.

### Train conditioned behavior

A behavior-cloning baseline minimizes
$$L_{\mathrm{BC}}=-\mathbb E_{(o,a,g)\sim D}\log\pi_\theta(a\mid o,g),$$
where $g$ is a language or image goal. The dataset paper evaluates multiple methods; this equation describes one baseline family, not a single prescribed BridgeData algorithm.


**Component practice**

- Supporting prerequisite: [Balance a Multi-Dataset Training Mixture](/problems/balance-multidataset-batch). Uses the bounded contract; no full paper reproduction is claimed.

### Test generalization

Report success $\hat p_s=n_s^{-1}\sum_{i\in s}\mathbf1[\mathrm{success}_i]$ per declared slice. Distinguish new task combinations from new environments and camera appearances. Dataset diversity and adaptation budget must be reported alongside results.


**Component practice**

- Evaluate Transfer by Environment Slice — unreviewed idea; contract and evaluator required.

## Implement the components

Runnable components and supporting prerequisites are attached to their matching execution-flow stages. Remaining titles are planned ideas requiring implementation and review.

- **Supporting prerequisite:** [Validate a Multimodal Robot Episode Schema](/problems/validate-robot-episodes).
- **Supporting prerequisite:** [Balance a Multi-Dataset Training Mixture](/problems/balance-multidataset-batch).

**Planned component problems:**

- Normalize Multi-Environment Robot Records — unreviewed idea; contract and evaluator required.
- Evaluate Transfer by Environment Slice — unreviewed idea; contract and evaluator required.

These exercises implement their stated contracts, not a complete paper reproduction.


## Why this matters on a robot

Shared manipulation data helps transfer beyond one lab setup. Camera shortcuts, inconsistent gripper conventions, and training/test overlap can exaggerate generalization.

## Sources and scope

[Primary paper](https://arxiv.org/abs/2308.12952) · [Open-access manuscript](https://arxiv.org/pdf/2308.12952)

This is an original explanation of selected mechanisms. Equations use the notation defined here; simplified teaching models are identified explicitly. Small component exercises do not reproduce the paper's full experiments. The local PDF is a research reference; its redistribution terms remain those recorded in the metadata.
