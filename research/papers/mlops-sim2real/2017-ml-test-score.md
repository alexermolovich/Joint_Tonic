---
schema_version: 1
paper_id: 2017-ml-test-score
title: >-
  The ML Test Score: A Rubric for ML Production Readiness and Technical Debt
  Reduction
authors:
  - Eric Breck
  - Shanqing Cai
  - Eric Nielsen
  - Michael Salib
  - D. Sculley
year: 2017
venue_or_status: IEEE Big Data 2017
primary_url: >-
  https://research.google/pubs/the-ml-test-score-a-rubric-for-ml-production-readiness-and-technical-debt-reduction/
pdf_url: 'https://storage.googleapis.com/gweb-research2023-media/pubtools/4156.pdf'
local_pdf: ./2017-ml-test-score.pdf
sha256: 8db5862dc7c7aaa2c55bb43bd42fc55531a0503782b7026b5811c00c98befd31
bytes: 500055
pages: 10
topics:
  - mlops
  - testing
  - monitoring
  - production-readiness
  - deployment-gates
modalities:
  - test-results
  - metrics
  - data-slices
  - operational-signals
track_role: supporting
open_access_status: open-access-proceedings
redistribution_note: Research copy only; verify the source license before redistribution.
execution_flow:
  title: Core execution flow
  description: >-
    Gather reproducible evidence, evaluate named checks, and decide whether a
    particular release satisfies its declared contract.
  nodes:
    - id: stage-1
      title: Collect versioned evidence
      detail: >-
        Associate each test with the exact data, model, runtime, and evaluation
        setup.
      column: 0
      row: 0
      section: Collect versioned evidence
      problem_slugs:
        - record-artifact-lineage
      planned_problems: []
    - id: stage-2
      title: Evaluate explicit checks
      detail: 'Distinguish pass, fail, and missing evidence for each requirement.'
      column: 1
      row: 0
      section: Evaluate explicit checks
      problem_slugs:
        - robot-ml-readiness-score
      planned_problems: []
    - id: stage-3
      title: Gate the candidate release
      detail: Require the critical checks to pass and expose every rejection reason.
      column: 2
      row: 0
      section: Gate the candidate release
      problem_slugs:
        - edge-inference-release-gate
        - slice-infrastructure-release-gate
        - physical-ai-incident-triage
      planned_problems: []
  edges:
    - from: stage-1
      to: stage-2
      label: evidence artifacts
    - from: stage-2
      to: stage-3
      label: check results
---

## Core paper explanation

The ML Test Score organizes production readiness around tests for data, models, infrastructure, and monitoring. It argues that offline model accuracy alone is insufficient evidence that an ML system is reliable. A useful implementation keeps individual checks and their evidence visible instead of hiding them behind one aggregate number. The logical gates below are teaching formalizations, not a replacement for the paper’s original rubric.

## Execution flow

Gather reproducible evidence, evaluate named checks, and decide whether a particular release satisfies its declared contract.

### Collect versioned evidence

Represent check $i$ as $(v_i,e_i,t_i)$: tested version, evidence artifact, and evaluation time. A release decision is meaningful only if evidence corresponds to the candidate being released. For example,

$$
\mathrm{current}_i=\mathbf1[v_i=v_{\mathrm{candidate}}]\mathbf1[t_i\ge t_{\mathrm{required}}].
$$

This simple freshness contract must be defined per test; not every check expires on the same schedule.


**Component practice**

- Supporting prerequisite: [Record Dataset, Transform, Model, and Evaluator Lineage](/problems/record-artifact-lineage). Uses the bounded contract; no full paper reproduction is claimed.

### Evaluate explicit checks

For quality $q$ and measured tail latency $\ell$, a small release contract may require

$$
q\ge q_{\min},\qquad \ell\le\ell_{\max}.
$$

Threshold direction, metric slice, hardware class, and sample count are part of each condition. Missing measurements are not zero-cost passes. Other checks concern data contracts, monitoring, rollback, and reproducibility rather than model scores.


**Component practice**

- Runnable component: [Score a Robot ML System for Production Readiness](/problems/robot-ml-readiness-score). Uses the bounded contract; no full paper reproduction is claimed.

### Gate the candidate release

For required checks $C$,

$$
\mathrm{release}=\bigwedge_{i\in C}(\mathrm{status}_i=\mathrm{pass}).
$$

[Gate an Edge Model with Accuracy and Latency](/problems/edge-inference-release-gate) implements a bounded quality/latency gate. It does not implement the full ML Test Score rubric. A deterministic list of reasons is more useful for remediation than a single unexplained false value.


**Component practice**

- Runnable component: [Gate an Edge Model with Accuracy and Latency](/problems/edge-inference-release-gate). Implements the bounded learning contract linked here, not the complete paper.
- Runnable component: [Gate a Release on Slice and Infrastructure Tests](/problems/slice-infrastructure-release-gate). Uses the bounded contract; no full paper reproduction is claimed.
- Runnable component: [Triage a Physical-AI Deployment Incident](/problems/physical-ai-incident-triage). Uses the bounded contract; no full paper reproduction is claimed.

## Implement the components

Runnable components and supporting prerequisites are attached to their matching execution-flow stages. Remaining titles are planned ideas requiring implementation and review.

- **Supporting prerequisite:** [Record Dataset, Transform, Model, and Evaluator Lineage](/problems/record-artifact-lineage).
- **Runnable component:** [Score a Robot ML System for Production Readiness](/problems/robot-ml-readiness-score).
- **Runnable component:** [Gate an Edge Model with Accuracy and Latency](/problems/edge-inference-release-gate).
- **Runnable component:** [Gate a Release on Slice and Infrastructure Tests](/problems/slice-infrastructure-release-gate).
- **Runnable component:** [Triage a Physical-AI Deployment Incident](/problems/physical-ai-incident-triage).

These exercises implement their stated contracts, not a complete paper reproduction.


## Why this matters on a robot

Robot readiness also depends on calibration, control-loop timing, sensor health, and recovery behavior. A model can pass an aggregate benchmark while violating a critical operating slice. Tests must describe the operating envelope and the evidence supporting it.

## Sources and scope

[Primary paper](https://research.google/pubs/the-ml-test-score-a-rubric-for-ml-production-readiness-and-technical-debt-reduction/) · [Open-access manuscript](https://storage.googleapis.com/gweb-research2023-media/pubtools/4156.pdf)

This is an original explanation of selected mechanisms. Equations use the notation defined here; simplified teaching models are identified explicitly. Small component exercises do not reproduce the paper's full experiments. The local PDF is a research reference; its redistribution terms remain those recorded in the metadata.
