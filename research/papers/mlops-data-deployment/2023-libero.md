---
schema_version: 1
paper_id: 2023-libero
title: 'LIBERO: Benchmarking Knowledge Transfer for Lifelong Robot Learning'
authors:
  - 'Liu, Bo'
  - 'Zhu, Yifeng'
  - 'Gao, Chongkai'
  - 'Feng, Yihao'
  - 'Liu, Qiang'
  - 'Zhu, Yuke'
  - 'Stone, Peter'
year: 2023
venue_or_status: >-
  Author-deposited arXiv manuscript; final venue not asserted by this
  acquisition card.
primary_url: 'https://arxiv.org/abs/2306.03310'
pdf_url: 'https://arxiv.org/pdf/2306.03310'
local_pdf: ./2023-libero.pdf
sha256: ff7d943e2eb37760df684f3ae2931a5a35ef8ea465bd387e62afe49507b8e414
bytes: 37420885
pages: 44
topics:
  - mlops-data-deployment
  - libero
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
      title: Define a task sequence
      detail: 'Choose task families, order, demonstrations, and initial states.'
      column: 0
      row: 0
      section: Define a task sequence
      problem_slugs:
        - libero-continual-task-schedule
        - libero-semantic-scene-factors
      planned_problems: []
    - id: stage-2
      title: Train and retain evaluation history
      detail: Evaluate earlier tasks after each learning stage.
      column: 1
      row: 0
      section: Train and retain evaluation history
      problem_slugs:
        - libero-evaluation-history-matrix
      planned_problems: []
    - id: stage-3
      title: Measure transfer and forgetting
      detail: Summarize the matrix without hiding task-level outcomes.
      column: 2
      row: 0
      section: Measure transfer and forgetting
      problem_slugs:
        - libero-forward-backward-transfer
      planned_problems: []
  edges:
    - from: stage-1
      to: stage-2
      label: ordered tasks
    - from: stage-2
      to: stage-3
      label: success matrix
---

## Core paper explanation

LIBERO studies knowledge transfer and lifelong robot learning using controlled manipulation task suites. Spatial, object, goal, and broader task variations separate different sources of transfer difficulty.

## Execution flow

Follow the data through the mechanism. Training objectives and inference behavior are distinguished in the linked explanations.

### Define a task sequence

Let tasks be $\mathcal T_1,\ldots,\mathcal T_K$. The sequence order is part of the experiment because sequential adaptation can depend strongly on prior tasks. Keep demonstrations, evaluation seeds, and initial-state definitions versioned.


**Component practice**

- [Build a Continual-Learning Task Sequence](/problems/libero-continual-task-schedule).
- [Separate Task Semantics from Scene Variation](/problems/libero-semantic-scene-factors).


### Train and retain evaluation history

Define $R_{ij}$ as success on task $j$ after learning through task $i$. This evaluation matrix distinguishes acquisition from retention. Joint training, sequential fine-tuning, and replay methods require separate resource/data accounting.


**Component practice**

- [Record a Continual-Learning Evaluation Matrix](/problems/libero-evaluation-history-matrix).


### Measure transfer and forgetting

Teaching summaries include final average $K^{-1}\sum_jR_{Kj}$ and forgetting
$$F=\frac1{K-1}\sum_{j<K}\left(\max_{j\le i\le K}R_{ij}-R_{Kj}\right).$$
State the exact index range and protocol when reproducing published metrics; these formulas explain the distinction, not a replacement for every LIBERO report. Inspect individual tasks as well as averages.


**Component practice**

- [Compute a Forward and Backward Transfer Matrix](/problems/libero-forward-backward-transfer).


## Implement the components

Each execution-flow node links the matching runnable component or names its planned problem. Planned titles are not runnable; labels distinguish reviewed drafts from unreviewed ideas.


**Component status:**

- [Build a Continual-Learning Task Sequence](/problems/libero-continual-task-schedule).
- [Separate Task Semantics from Scene Variation](/problems/libero-semantic-scene-factors).
- [Record a Continual-Learning Evaluation Matrix](/problems/libero-evaluation-history-matrix).
- [Compute a Forward and Backward Transfer Matrix](/problems/libero-forward-backward-transfer).

These bounded exercises do not claim to reproduce the complete paper or its benchmark results.

## Scope of the runnable components

The runnable tasks define a deterministic demonstration budget and task order, annotation-based semantic groups, an idempotent stage/task evaluation history, and explicit forward/backward transfer summaries. Forgetting uses complete observed post-learning histories including the final stage. These are declared longitudinal reporting conventions, not claims to reproduce every LIBERO metric or task generator.

## Why this matters on a robot

A robot should gain new skills without losing previously reliable ones. Changes in task order, evaluation seeds, or demonstration budgets can produce apparent algorithm gains that are actually protocol differences.

## Sources and scope

[Primary paper](https://arxiv.org/abs/2306.03310) · [Open-access manuscript](https://arxiv.org/pdf/2306.03310)

This is an original explanation of selected mechanisms. Equations use the notation defined here; simplified teaching models are identified explicitly. Small component exercises do not reproduce the paper's full experiments. The local PDF is a research reference; its redistribution terms remain those recorded in the metadata.
