---
schema_version: 1
paper_id: 2020-data-regularized-q
title: >-
  Image Augmentation Is All You Need: Regularizing Deep Reinforcement Learning
  from Pixels
authors:
  - 'Kostrikov, Ilya'
  - 'Yarats, Denis'
  - 'Fergus, Rob'
year: 2020
venue_or_status: >-
  Author-deposited arXiv manuscript; final venue not asserted by this
  acquisition card.
primary_url: 'https://arxiv.org/abs/2004.13649'
pdf_url: 'https://arxiv.org/pdf/2004.13649'
local_pdf: ./2020-data-regularized-q.pdf
sha256: 5860ea8ff5584b78010d55952caa9ab7e5c8d71b2e3a336b7288406098fccef4
bytes: 1291799
pages: 22
topics:
  - robot-learning-rl
  - data-regularized-q
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
      title: Augment visual observations
      detail: Apply transformations intended to preserve action value.
      column: 0
      row: 0
      section: Augment visual observations
      problem_slugs:
        - drq-seeded-random-shift
      planned_problems: []
    - id: stage-2
      title: Average augmented targets
      detail: Reduce target variability across transformed successor views.
      column: 1
      row: 0
      section: Average augmented targets
      problem_slugs:
        - drq-augmented-bellman-targets
      planned_problems: []
    - id: stage-3
      title: Fit multiple current views
      detail: Train the critic to agree across augmentations.
      column: 2
      row: 0
      section: Fit multiple current views
      problem_slugs:
        - drq-multiview-critic-loss
        - shift-bucket-performance
      planned_problems: []
  edges:
    - from: stage-1
      to: stage-2
      label: augmented next observations
    - from: stage-2
      to: stage-3
      label: shared targets
---

## Core paper explanation

DrQ regularizes pixel-based reinforcement learning with image augmentations that should preserve task state. Averaging value targets and fitting multiple augmented views improves visual learning without a separate representation-pretraining objective.

## Execution flow

Follow the data through the mechanism. Training objectives and inference behavior are distinguished in the linked explanations.

### Augment visual observations

Let $f(o,\nu)$ be an image transform with sampled parameter $\nu$. The intended invariance is $Q(f(o,\nu),a)\approx Q(o,a)$. Random shifts can satisfy this approximately; transformations that remove the manipulated object or change geometry may violate it.


**Implement this component:** [Apply a Seeded Random-Shift Augmentation](/problems/drq-seeded-random-shift).


### Average augmented targets

The core target construction is
$$y=r+\gamma(1-d)\frac1K\sum_{k=1}^K V_{\mathrm{target}}(f(o',\nu'_k)).$$
Here $V_{\mathrm{target}}$ denotes the selected base algorithm's action/value target, including entropy terms when using SAC. The same physical transition supplies every view.


**Implement this component:** [Average Augmented Bellman Targets](/problems/drq-augmented-bellman-targets).


### Fit multiple current views

Use
$$L_Q=\frac1M\sum_{m=1}^M(Q(f(o,\nu_m),a)-y)^2.$$
Keep image histories temporally consistent when applying transforms. Augmentation is a hypothesis about invariance, not a guarantee that every visual perturbation preserves the control problem.


**Implement this component:** [Compute a Multi-View Critic Regression Loss](/problems/drq-multiview-critic-loss).

**Implement this component:** [Evaluate Policy Robustness to Visual Shifts](/problems/shift-bucket-performance). Group supplied comparable per-scenario errors by declared visual-shift buckets, preserving missing buckets. This diagnostic does not train a policy or reproduce DrQ robustness benchmarks.


## Implement the components

Exercises are attached to the corresponding execution stages and mathematical explanations above. Runnable links implement only their stated component scope. Planned titles are original authoring ideas, not reviewed contracts, runnable tasks, or claims of a reproduced paper. They enter the approved curriculum only through blueprint review.

- **Augment visual observations:** [Apply a Seeded Random-Shift Augmentation](/problems/drq-seeded-random-shift).
- **Average augmented targets:** [Average Augmented Bellman Targets](/problems/drq-augmented-bellman-targets).
- **Fit multiple current views:** [Compute a Multi-View Critic Regression Loss](/problems/drq-multiview-critic-loss); [Evaluate Policy Robustness to Visual Shifts](/problems/shift-bucket-performance).

## Why this matters on a robot

Visual regularization can reduce camera-background overfitting. Cropping away a contact point or independently shifting stacked frames can create false motion and harm control.

## Sources and scope

[Primary paper](https://arxiv.org/abs/2004.13649) · [Open-access manuscript](https://arxiv.org/pdf/2004.13649)

This is an original explanation of selected mechanisms. Equations use the notation defined here; simplified teaching models are identified explicitly. Small component exercises do not reproduce the paper's full experiments. The local PDF is a research reference; its redistribution terms remain those recorded in the metadata.
