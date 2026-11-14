---
schema_version: 1
paper_id: 2019-mlperf-inference
title: MLPerf Inference Benchmark
authors:
  - Vijay Janapa Reddi et al. (MLPerf consortium)
year: 2019
venue_or_status: arXiv 2019; industry benchmark paper
primary_url: 'https://arxiv.org/abs/1911.02549'
pdf_url: 'https://arxiv.org/pdf/1911.02549'
local_pdf: ./2019-mlperf-inference.pdf
sha256: ab71faac2c06fa5c317f559e3e96c7baa24a7d15bcf757efcee085ee1a3a1efd
bytes: 1185996
pages: 15
topics:
  - benchmarking
  - inference
  - latency
  - throughput
  - reproducibility
modalities:
  - queries
  - timing-events
  - predictions
  - quality-metrics
track_role: supporting
open_access_status: open-access-preprint
redistribution_note: Research copy only; verify the source license before redistribution.
execution_flow:
  title: Core execution flow
  description: >-
    Choose a workload and arrival scenario, capture end-to-end query timing, and
    accept performance results only when quality and benchmark conditions hold.
  nodes:
    - id: stage-1
      title: Specify the load scenario
      detail: Define how requests arrive and what counts as a completed query.
      column: 0
      row: 0
      section: Specify the load scenario
      problem_slugs:
        - simulate-inference-load
      planned_problems: []
    - id: stage-2
      title: Measure query performance
      detail: 'Record latency distributions, completed work, and measurement scope.'
      column: 1
      row: 0
      section: Measure query performance
      problem_slugs:
        - inference-latency-percentiles
      planned_problems:
        - Compute Inference Throughput from Query Traces
    - id: stage-3
      title: Apply quality and latency gates
      detail: >-
        Reject configurations that trade away required correctness or miss
        scenario limits.
      column: 2
      row: 0
      section: Apply quality and latency gates
      problem_slugs:
        - edge-inference-release-gate
        - reject-invalid-benchmark-runs
      planned_problems: []
  edges:
    - from: stage-1
      to: stage-2
      label: query trace
    - from: stage-2
      to: stage-3
      label: quality and timing
---

## Core paper explanation

MLPerf Inference defines benchmark workloads and load scenarios so inference systems can be compared under quality and performance constraints. The2019paper distinguishes single-stream, multistream, server, and offline execution: the query arrival process and performance metric change across these scenarios. Its central lesson is that throughput and latency are meaningful only with a specified workload and quality target.

## Execution flow

Choose a workload and arrival scenario, capture end-to-end query timing, and accept performance results only when quality and benchmark conditions hold.

### Specify the load scenario

A server-style teaching load generator can model exponential interarrival times

$$
\Delta t\sim\operatorname{Exponential}(\lambda),
\qquad\mathbb E[\Delta t]=1/\lambda.
$$

Single-stream issues the next query after the preceding one completes; offline submits a large batch for throughput. These workloads stress different system behavior. The historical paper is not a substitute for checking the rules of a specific later benchmark release.


**Component practice**

- Runnable component: [Simulate Single-Stream and Server Load](/problems/simulate-inference-load). Implements the explicit bounded contract, not the complete source system.


### Measure query performance

For request arrival $a_i$ and completion $c_i$, latency is $\ell_i=c_i-a_i$. A simple empirical percentile estimator on sorted latencies is

$$
\hat q_p=\ell_{(\lceil pN\rceil)},\qquad
\mathrm{throughput}=N_{\mathrm{completed}}/T.
$$

This estimator is an educational definition; an official benchmark may impose additional confidence, duration, and validity requirements. Device synchronization and host-device transfers must be included or excluded consistently.


**Component practice**

- Runnable component: [Compute p50, p90, and p99 Inference Latency](/problems/inference-latency-percentiles). Implements the bounded learning contract linked here, not the complete paper.
- Compute Inference Throughput from Query Traces — unreviewed idea; contract and evaluator required.


### Apply quality and latency gates

A bounded release condition is

$$
\mathrm{pass}=\mathbf1[q\ge q_{\min}]\land\mathbf1[\hat q_p\le L_{\max}].
$$

[Gate an Edge Model with Accuracy and Latency](/problems/edge-inference-release-gate) implements this kind of explicit contract across supplied hardware records. It is not an MLPerf submission checker. Record model, runtime, device, precision, and workload versions with every reported score.


**Component practice**

- Runnable component: [Gate an Edge Model with Accuracy and Latency](/problems/edge-inference-release-gate). Implements the bounded learning contract linked here, not the complete paper.
- Runnable component: [Reject Invalid Benchmark Runs](/problems/reject-invalid-benchmark-runs). Implements the explicit bounded contract, not the complete source system.


## Implement the components

Execution-flow nodes link runnable component exercises. Any additional research ideas remain explicitly labeled as future work and do not imply a complete paper reproduction.

- **Runnable component:** [Compute p50, p90, and p99 Inference Latency](/problems/inference-latency-percentiles).
- **Runnable component:** [Gate an Edge Model with Accuracy and Latency](/problems/edge-inference-release-gate).

**Component implementation map:**

- Runnable component: [Simulate Single-Stream and Server Load](/problems/simulate-inference-load). Implements the explicit bounded contract, not the complete source system.
- Compute Inference Throughput from Query Traces — unreviewed idea; contract and evaluator required.
- Runnable component: [Reject Invalid Benchmark Runs](/problems/reject-invalid-benchmark-runs). Implements the explicit bounded contract, not the complete source system.

These bounded exercises do not claim to reproduce the complete paper or its benchmark results.

## Why this matters on a robot

A robot often cares about late frames and missed control deadlines, not just average throughput. Camera queues, preprocessing, and scheduling can dominate tail latency. Benchmark the intended deployment workload and report accuracy changes when changing precision or optimization settings.

## Sources and scope

[Primary paper](https://arxiv.org/abs/1911.02549) · [Open-access manuscript](https://arxiv.org/pdf/1911.02549)

This is an original explanation of selected mechanisms. Equations use the notation defined here; simplified teaching models are identified explicitly. Small component exercises do not reproduce the paper's full experiments. The local PDF is a research reference; its redistribution terms remain those recorded in the metadata.
