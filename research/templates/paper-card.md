---
schema_version: 1
paper_id: "year-short-title"
title: "Full paper title"
authors:
  - "Author One"
year: 2026
venue_or_status: "Conference, journal, or preprint status"
primary_url: "https://canonical.example/paper"
pdf_url: "https://canonical.example/paper.pdf"
local_pdf: "./year-short-title.pdf"
sha256: "64-lowercase-hex-characters"
bytes: 0
pages: 0
topics:
  - "topic-slug"
modalities:
  - "rgb"
track_role: "foundation | core | advanced | supporting"
open_access_status: "open-access-preprint | open-access-proceedings | unknown"
redistribution_note: "Research copy only; verify the source license before redistribution."
execution_flow:
  title: "Follow the method from inputs to outputs"
  description: "Name which branches are training, inference, or evaluation."
  nodes:
    - id: inputs
      title: "Prepare inputs"
      detail: "Explain the input contract."
      column: 0
      row: 0
      section: "Input contract"
      problem_slugs: []
      planned_problems: []
    - id: component
      title: "Apply the core mechanism"
      detail: "Explain the transformation this component performs."
      column: 1
      row: 0
      section: "Core mechanism"
      problem_slugs: []
  edges:
    - from: inputs
      to: component
      label: "Validated inputs"
---

# Full paper title

## Core paper explanation

In 3–6 original sentences, state the problem, the paper's central mechanism, why it matters to physical AI, and the most teachable implementation surface.

## Execution flow

Explain how data passes through the graph above. Describe training and inference separately and name any conditioning inputs, feedback, and evaluation paths. Use this paper's actual method, not a generic ML pipeline. Graph nodes are ordered in the recommended learning sequence. Each `section` must exactly match a plain-text H2/H3 heading below. Give nodes distinct nonnegative `column`/`row` positions (prefer at most three columns); label edges with tensors or signals. Use only existing runnable slugs in `problem_slugs`. Attach future exercise titles to the particular component using `planned_problems: ["Exact curriculum or blueprint title"]`; these are displayed as implementation pending, without runnable URLs. Where no reviewed blueprint exists, an original paper-specific component title is an idea rather than a commitment. An exact unambiguous title becomes runnable automatically once its complete problem is published. Keep the same associations beside the explanation's math, distinguish supporting prerequisites, and remove stale planned bullets when the component becomes available.

## Input contract

Define observations/data, shapes, units, frames, normalization, batching, time and masks as applicable. Explain assumptions near first use.

## Core mechanism

Begin with intuition, then use `$...$` and `$$...$$` for essential equations. Define every symbol and connect the algebra to what executes in code. Include a worked small numerical/tensor example when it clarifies the implementation. Link the associated runnable problem directly here using `[Problem title](/problems/existing-slug)`, and explain its scope/deviations. Do not leave this placeholder link in a published card.

Repeat a named section for each model or systems stage. Preserve meaningful mathematical depth; a citation or a list of model names is not an explanation. Distinguish paper-defined math from educational choices and operational extensions.

## Contribution

- What changed relative to prior work.
- What evidence supports the contribution.
- What the paper does **not** establish.

## Prerequisite concepts

- Concept and suggested Joint Tonic prerequisite problem.

## Method map

| Component | Input | Output | Core invariant | Good exercise boundary |
|---|---|---|---|---|
| Example component | Shape/unit/frame | Shape/unit/frame | Testable property | Atomic implementation |

## Data and evaluation

- Datasets/robot embodiments and their roles.
- Metrics and protocol.
- Compute or hardware assumptions that materially affect interpretation.
- Difference between a small educational reproduction and the reported experiment.

## Limitations and failure modes

- Paper-stated limitations.
- Important operational risks or out-of-distribution cases.
- Licensing/data/deployment constraints.

## Implementation decomposition

1. First atomic mechanism.
2. Second component.
3. Integration.
4. Evaluation and failure analysis.
5. Packaging, deployment, or monitoring extension.

## Problem blueprints

### Problem: Stable problem title

- **Type:** function | component | debug | pipeline | optimization | experiment | incident
- **Difficulty:** easy | medium | hard | research
- **Learning objective:** One observable skill.
- **Inputs:** Shapes, dtypes, units, frames, timestamps, and bounds.
- **Outputs:** Shapes, dtypes, units, frames, and ordering.
- **Fixture:** Synthetic or licensed source.
- **Grading:** Deterministic invariants, tolerances, metrics, performance class, and hidden-edge families.
- **Paper deviation:** What is simplified or omitted.

Repeat for 3–5 useful problems, normally including one evaluation/failure-analysis or MLOps task.

## MLOps and deployment extensions

- Data validation/lineage opportunity.
- Reproducible training/evaluation opportunity.
- Inference optimization/edge constraint.
- Monitoring, drift, rollback, or safety scenario.

## Canonical sources

- [Primary landing page](https://canonical.example/paper)
- [Open-access PDF](https://canonical.example/paper.pdf)
- [Official code or project page](https://canonical.example/project) when available
