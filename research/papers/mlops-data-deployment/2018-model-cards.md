---
schema_version: 1
paper_id: 2018-model-cards
title: Model Cards for Model Reporting
authors:
  - 'Mitchell, Margaret'
  - 'Wu, Simone'
  - 'Zaldivar, Andrew'
  - 'Barnes, Parker'
  - 'Vasserman, Lucy'
  - 'Hutchinson, Ben'
  - 'Spitzer, Elena'
  - 'Raji, Inioluwa Deborah'
  - 'Gebru, Timnit'
year: 2018
venue_or_status: >-
  Author-deposited arXiv manuscript; final venue not asserted by this
  acquisition card.
primary_url: 'https://arxiv.org/abs/1810.03993'
pdf_url: 'https://arxiv.org/pdf/1810.03993'
local_pdf: ./2018-model-cards.pdf
sha256: a4049cdc78c3d635bdfb5165e495b0672d85690d66ccd6f149079d6e11e64aa1
bytes: 995470
pages: 10
topics:
  - mlops-data-deployment
  - model-cards
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
      title: Identify the model and use
      detail: 'Record version, training context, and supported deployment conditions.'
      column: 0
      row: 0
      section: Identify the model and use
      problem_slugs: []
      planned_problems:
        - Validate a Model Card Schema
    - id: stage-2
      title: Evaluate meaningful slices
      detail: Report metrics by conditions relevant to intended use.
      column: 1
      row: 0
      section: Evaluate meaningful slices
      problem_slugs: []
      planned_problems:
        - Aggregate Metrics by Operational Slice
    - id: stage-3
      title: Document release limitations
      detail: Connect results to intended and unsupported uses.
      column: 2
      row: 0
      section: Document release limitations
      problem_slugs:
        - edge-inference-release-gate
        - slice-infrastructure-release-gate
      planned_problems: []
  edges:
    - from: stage-1
      to: stage-2
      label: versioned model
    - from: stage-2
      to: stage-3
      label: slice evidence
---

## Core paper explanation

Model Cards proposes concise documentation of model identity, intended use, evaluation conditions, limitations, and relevant performance slices. It makes a release understandable beyond one aggregate benchmark number.

## Execution flow

Follow the data through the mechanism. Training objectives and inference behavior are distinguished in the linked explanations.

### Identify the model and use

A robotics release should identify weights, preprocessing, action decoder, training data versions, and hardware assumptions. Treat the model artifact as a tuple $(W,P,D,R)$ of weights, preprocessing, decoder, and runtime. This is a teaching release contract, not the paper's mathematical notation.


**Component practice**

- Validate a Model Card Schema — unreviewed idea; contract and evaluator required.

### Evaluate meaningful slices

For slice $s$ with $n_s$ trials, success rate is
$$\hat p_s=\frac1{n_s}\sum_{i\in s}\mathbf1[\mathrm{success}_i].$$
Report denominators and uncertainty, especially for small or intersectional slices. Robotics slices might include lighting, object category, camera, and embodiment; human-facing applications also require appropriate demographic analysis.


**Component practice**

- Aggregate Metrics by Operational Slice — unreviewed idea; contract and evaluator required.

### Document release limitations

A teaching release gate can require $\bigwedge_k[m_k\in\mathcal A_k]$, with declared acceptable regions $\mathcal A_k$. This gate is our implementation extension, not a universal model-card standard. Keep unresolved failures and out-of-scope uses visible alongside successful metrics.


**Component practice**

- Supporting prerequisite: [Gate an Edge Model with Accuracy and Latency](/problems/edge-inference-release-gate). Practices the stated data or mathematical operation; it does not implement this paper-specific stage in full.
- Supporting prerequisite: [Gate a Release on Slice and Infrastructure Tests](/problems/slice-infrastructure-release-gate). Uses the bounded contract; no full paper reproduction is claimed.

## Implement the components

Runnable components and supporting prerequisites are attached to their matching execution-flow stages. Remaining titles are planned ideas requiring implementation and review.

- **Supporting prerequisite:** [Gate an Edge Model with Accuracy and Latency](/problems/edge-inference-release-gate).
- **Supporting prerequisite:** [Gate a Release on Slice and Infrastructure Tests](/problems/slice-infrastructure-release-gate).

**Planned component problems:**

- Validate a Model Card Schema — unreviewed idea; contract and evaluator required.
- Aggregate Metrics by Operational Slice — unreviewed idea; contract and evaluator required.

These exercises implement their stated contracts, not a complete paper reproduction.


## Why this matters on a robot

A model card helps determine whether a policy evaluated on one robot and camera is suitable elsewhere. Aggregate success can conceal critical weak slices; documentation should preserve those limitations rather than imply universal reliability.

## Sources and scope

[Primary paper](https://arxiv.org/abs/1810.03993) · [Open-access manuscript](https://arxiv.org/pdf/1810.03993)

This is an original explanation of selected mechanisms. Equations use the notation defined here; simplified teaching models are identified explicitly. Small component exercises do not reproduce the paper's full experiments. The local PDF is a research reference; its redistribution terms remain those recorded in the metadata.
