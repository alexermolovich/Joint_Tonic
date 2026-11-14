---
schema_version: 1
paper_id: "2015-hidden-technical-debt"
title: "Hidden Technical Debt in Machine Learning Systems"
authors:
  - "D. Sculley"
  - "Gary Holt"
  - "Daniel Golovin"
  - "Eugene Davydov"
  - "Todd Phillips"
  - "Dietmar Ebner"
  - "Vinay Chaudhary"
  - "Michael Young"
  - "Jean-Francois Crespo"
  - "Dan Dennison"
year: 2015
venue_or_status: "NeurIPS 2015"
primary_url: "https://proceedings.neurips.cc/paper/2015/hash/86df7dcfd896fcaf2674f757a2463eba-Abstract.html"
pdf_url: "https://proceedings.neurips.cc/paper_files/paper/2015/file/86df7dcfd896fcaf2674f757a2463eba-Paper.pdf"
local_pdf: "./2015-hidden-technical-debt.pdf"
sha256: "1a67da09a8bd5ba9a3577176e30aa2fbd88534e6baf0bc31522b4999f643d2a1"
bytes: 165614
pages: 9
topics:
  - "mlops"
  - "technical-debt"
  - "dependency-management"
  - "monitoring"
  - "production-ml"
modalities:
  - "system-graphs"
  - "metadata"
  - "operational-metrics"
track_role: "foundation"
open_access_status: "open-access-proceedings"
redistribution_note: "Research copy only; verify the source license before redistribution."
---

## Agent brief

Use this paper to teach why a good model can still create a fragile robot product. The implementation target is a small analyzer for ML-system dependencies and operational risks, not a model-training exercise.

## Contribution

The paper names recurring ML-specific debt patterns: entangled signals, hidden feedback loops, undeclared data consumers, glue code, configuration debt, and changes in the outside world. It turns maintainability into a system-level design concern.

## Prerequisite concepts

- Directed graphs and cycle detection
- Basic ML training and inference lifecycle
- Configuration files and dependency metadata
- Unit versus integration testing

## Method map

| Component | Input | Output | Core invariant | Good exercise boundary |
| --- | --- | --- | --- | --- |
| Dependency inventory | Pipeline and ownership metadata | Typed system graph | Every reference resolves to a declared node | Parse and validate one system description |
| Debt analyzer | System graph and monitor coverage | Ranked findings with evidence | Every finding names the rule and supporting path | Implement cycle, fan-out, or ownership checks independently |

- Model and data dependency graph
- Consumers and producers of features, labels, and predictions
- Configuration surface and ownership metadata
- Feedback-loop and change-risk analysis
- Monitoring coverage map

## Data and evaluation

Use synthetic pipeline graphs with known cycles, shared features, undeclared consumers, and intentionally missing monitors. Grade against expected findings, false-positive count, and deterministic severity scoring.

## Limitations and failure modes

This is a conceptual systems paper rather than an empirical benchmark. Risk categories require local judgment, and a static graph cannot reveal every runtime coupling or organizational failure.

## Implementation decomposition

1. Define a typed node/edge schema for data, models, services, and monitors.
2. Parse a pipeline description and validate references.
3. Detect cycles, high-fan-out dependencies, and unowned nodes.
4. Apply explicit risk rules with human-readable evidence.
5. Produce a ranked debt report and remediation hints.

## Problem blueprints

| Title | Type | Difficulty | Inputs | Outputs | Grading |
| --- | --- | --- | --- | --- | --- |
| Dependency Blast Radius | Graph algorithm | Medium | Typed DAG and changed node | Sorted affected nodes and distances | Exact reachability, stable ordering, edge cases |
| Feedback Loop Detector | Graph algorithm | Medium | Directed production graph | Cycles with supporting edges | Finds all expected cycles without duplicates |
| Debt Risk Rubric | Systems reasoning | Hard | Graph plus ownership/monitor metadata | Per-risk evidence and severity | Rule accuracy, explanations, deterministic total score |

## Visual teaching plan

- Interactive dependency graph where selecting a changed feature reveals its blast radius.
- Toggleable overlays for feedback loops, undeclared consumers, missing owners, and missing monitors.
- Before/after architecture diagram showing glue code replaced by explicit component contracts.
- Risk matrix linking each detected debt pattern to likelihood, impact, evidence, and mitigation.

## MLOps and deployment extensions

Add robot fleet, sensor firmware, calibration, simulator, safety monitor, and teleoperation nodes. Treat logged actions and later training labels as a possible feedback loop. Require owners and rollback plans for every on-robot model consumer.

## Canonical sources

- [Official proceedings page](https://proceedings.neurips.cc/paper/2015/hash/86df7dcfd896fcaf2674f757a2463eba-Abstract.html)
- [Official PDF](https://proceedings.neurips.cc/paper_files/paper/2015/file/86df7dcfd896fcaf2674f757a2463eba-Paper.pdf)

