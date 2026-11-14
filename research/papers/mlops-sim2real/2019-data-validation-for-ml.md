---
schema_version: 1
paper_id: 2019-data-validation-for-ml
title: Data Validation for Machine Learning
authors:
  - Eric Breck
  - Marty Zinkevich
  - Neoklis Polyzotis
  - Steven Whang
  - Sudip Roy
year: 2019
venue_or_status: SysML 2019
primary_url: 'https://research.google/pubs/data-validation-for-machine-learning/'
pdf_url: 'https://mlsys.org/Conferences/2019/doc/2019/167.pdf'
local_pdf: ./2019-data-validation-for-ml.pdf
sha256: 4c26718460681e3cd8a2be65308f85352af1be46aef84cf749903f9387381f53
bytes: 435587
pages: 14
topics:
  - data-quality
  - schema-inference
  - anomaly-detection
  - training-serving-skew
  - monitoring
modalities:
  - tabular-features
  - distributions
  - schemas
  - robot-episode-metadata
track_role: core
open_access_status: open-access-proceedings
redistribution_note: Research copy only; verify the source license before redistribution.
execution_flow:
  title: Core execution flow
  description: >-
    Infer or declare a schema, validate examples and dataset statistics, then
    review anomalies and version accepted changes.
  nodes:
    - id: stage-1
      title: Define feature contracts
      detail: 'Declare presence, type, shape, domain, and range requirements.'
      column: 0
      row: 0
      section: Define feature contracts
      problem_slugs:
        - validate-robot-episodes
        - infer-robot-episode-schema
        - robot-feature-anomalies
      planned_problems: []
    - id: stage-2
      title: Compare statistics and slices
      detail: Identify distribution changes and training-serving differences.
      column: 1
      row: 0
      section: Compare statistics and slices
      problem_slugs:
        - compare-training-serving-distributions
        - sensor-timestamp-calibration-skew
      planned_problems: []
    - id: stage-3
      title: Review and version anomalies
      detail: >-
        Distinguish bad data from an intentional schema change and preserve the
        decision.
      column: 2
      row: 0
      section: Review and version anomalies
      problem_slugs:
        - critical-data-anomaly-gate
      planned_problems: []
  edges:
    - from: stage-1
      to: stage-2
      label: validated examples
    - from: stage-2
      to: stage-3
      label: named anomalies
---

## Core paper explanation

Data Validation for Machine Learning treats data checks as a first-class stage of the ML pipeline. It combines schemas, descriptive statistics, and comparisons across data slices or time to detect errors before they propagate into models. The implementation goal is actionable violations with feature identity and context, rather than an unexplained global anomaly score.

## Execution flow

Infer or declare a schema, validate examples and dataset statistics, then review anomalies and version accepted changes.

### Define feature contracts

For feature $j$, let contract $S_j$ define its acceptable domain $\mathcal D_j$. An elementary check is

$$
v_{ij}=\mathbf1[x_{ij}\notin\mathcal D_j].
$$

Missing values require a separate presence rule; zero may be a valid measurement. [Validate a Multimodal Robot Episode Schema](/problems/validate-robot-episodes) extends this idea to finite tensors, coordinate frames, units, and sensor timing under an explicit robotics contract.


**Component practice**

- Runnable component: [Validate a Multimodal Robot Episode Schema](/problems/validate-robot-episodes). Implements the bounded learning contract linked here, not the complete paper.
- Runnable component: [Infer a Schema from Robot Episodes](/problems/infer-robot-episode-schema). Uses the bounded contract; no full paper reproduction is claimed.
- Runnable component: [Detect Missing, Range, Domain, and Shape Anomalies](/problems/robot-feature-anomalies). Uses the bounded contract; no full paper reproduction is claimed.

### Compare statistics and slices

For a categorical feature with frequency vectors $p$ and $q$ over aligned categories, a simple comparison is

$$
d_\infty(p,q)=\max_c|p_c-q_c|.
$$

This illustrates a histogram-distance check; thresholds, missing categories, and sample size must be specified. The same distance can have different operational meaning for a rare critical label and a common nuisance category. Compare like-for-like slices and avoid silently changing histogram bins.


**Component practice**

- Runnable component: [Compare Training and Serving Distributions](/problems/compare-training-serving-distributions). Uses the bounded contract; no full paper reproduction is claimed.
- Runnable component: [Detect Sensor Timestamp and Calibration Skew](/problems/sensor-timestamp-calibration-skew). Uses the bounded contract; no full paper reproduction is claimed.

### Review and version anomalies

An anomaly record should identify the feature, violated rule, observed statistic, expected contract, source artifact, and severity. Updating the schema should create a new version rather than erase evidence that the prior contract failed. A mathematically small distribution change can still be operationally important when it affects a safety-critical slice.


**Component practice**

- Runnable component: [Block a Pipeline on Critical Data Anomalies](/problems/critical-data-anomaly-gate). Uses the bounded contract; no full paper reproduction is claimed.

## Implement the components

Runnable components and supporting prerequisites are attached to their matching execution-flow stages. Remaining titles are planned ideas requiring implementation and review.

- **Runnable component:** [Validate a Multimodal Robot Episode Schema](/problems/validate-robot-episodes).
- **Runnable component:** [Infer a Schema from Robot Episodes](/problems/infer-robot-episode-schema).
- **Runnable component:** [Detect Missing, Range, Domain, and Shape Anomalies](/problems/robot-feature-anomalies).
- **Runnable component:** [Compare Training and Serving Distributions](/problems/compare-training-serving-distributions).
- **Runnable component:** [Detect Sensor Timestamp and Calibration Skew](/problems/sensor-timestamp-calibration-skew).
- **Runnable component:** [Block a Pipeline on Critical Data Anomalies](/problems/critical-data-anomaly-gate).

These exercises implement their stated contracts, not a complete paper reproduction.


## Why this matters on a robot

Valid tensor shapes can hide swapped units, inconsistent clocks, or stale calibration. Dataset validation catches many such errors before training, but cannot infer every semantic contract automatically. Schema changes should be reviewed with knowledge of the robot and collection process.

## Sources and scope

[Primary paper](https://research.google/pubs/data-validation-for-machine-learning/) · [Open-access manuscript](https://mlsys.org/Conferences/2019/doc/2019/167.pdf)

This is an original explanation of selected mechanisms. Equations use the notation defined here; simplified teaching models are identified explicitly. Small component exercises do not reproduce the paper's full experiments. The local PDF is a research reference; its redistribution terms remain those recorded in the metadata.
