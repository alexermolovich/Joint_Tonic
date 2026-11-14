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
---

# Full paper title

## Agent brief

In 3–6 original sentences, state the problem, the paper's central mechanism, why it matters to physical AI, and the most teachable implementation surface.

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
