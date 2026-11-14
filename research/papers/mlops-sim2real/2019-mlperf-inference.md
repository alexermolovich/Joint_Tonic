---
schema_version: 1
paper_id: "2019-mlperf-inference"
title: "MLPerf Inference Benchmark"
authors:
  - "Vijay Janapa Reddi et al. (MLPerf consortium)"
year: 2019
venue_or_status: "arXiv 2019; industry benchmark paper"
primary_url: "https://arxiv.org/abs/1911.02549"
pdf_url: "https://arxiv.org/pdf/1911.02549"
local_pdf: "./2019-mlperf-inference.pdf"
sha256: "ab71faac2c06fa5c317f559e3e96c7baa24a7d15bcf757efcee085ee1a3a1efd"
bytes: 1185996
pages: 15
topics:
  - "benchmarking"
  - "inference"
  - "latency"
  - "throughput"
  - "reproducibility"
modalities:
  - "queries"
  - "timing-events"
  - "predictions"
  - "quality-metrics"
track_role: "supporting"
open_access_status: "open-access-preprint"
redistribution_note: "Research copy only; verify the source license before redistribution."
---

## Agent brief

Build a deterministic inference load generator and result checker. Teach realistic scenario semantics, latency percentiles, quality constraints, and auditability before optimizing a model.

## Contribution

MLPerf Inference defines representative tasks, realistic usage scenarios, quality targets, submission rules, and auditing mechanisms so results from diverse hardware/software systems remain comparable.

## Prerequisite concepts

- Descriptive statistics and percentiles
- Queues and arrival processes
- Accuracy or task-quality metrics
- Reproducible experiment configuration

## Essential theory

For request \(i\), latency is \(\ell_i=t_i^{\mathrm{complete}}-t_i^{\mathrm{issue}}\). Over a measured interval \([t_0,t_1]\), completed-query throughput is

$$
Q=\frac{N_{\mathrm{complete}}}{t_1-t_0}.
$$

A compliant run must satisfy both a task-quality constraint and the scenario's latency or throughput rule; optimizing one cannot silently invalidate the other.

## Method map

| Component | Input | Output | Core invariant | Good exercise boundary |
| --- | --- | --- | --- | --- |
| Load generator | Scenario, seed, rate, and duration | Timestamped request schedule | Scenario timing rules are deterministic and auditable | Simulate one inference scenario |
| Result recorder | Issue/completion events and predictions | Latency, throughput, and quality records | Every completion correlates with one issued request | Compute one benchmark result bundle |
| Compliance checker | Results and benchmark rules | Pass/fail plus violations | Quality and performance constraints are both enforced | Validate one submission |

- Workload and quality target
- Single-stream, multi-stream, server, and offline scenarios
- Query scheduler and load generator
- System-under-test timing interface
- Accuracy checker and compliance rules
- Submission metadata and audit trail

## Data and evaluation

Use timestamped synthetic requests plus known predictions. Evaluate exact scenario scheduling, latency distributions, throughput, target compliance, warmup exclusion, and repeatability from a fixed seed.

## Limitations and failure modes

Benchmark results apply only to declared workloads, rules, and system configurations. A high benchmark score does not prove fleet reliability, safety, energy efficiency, or robustness to changed sensor data.

## Implementation decomposition

1. Specify scenario configuration and quality target.
2. Generate requests and record issue/completion times.
3. Compute latency and throughput consistently.
4. Run task-quality checks.
5. Validate a self-contained result bundle.

## Problem blueprints

| Title | Type | Difficulty | Inputs | Outputs | Grading |
| --- | --- | --- | --- | --- | --- |
| Inference Percentiles | Metrics | Easy | Issue/completion timestamps | p50, p90, p99, throughput | Percentile convention, units, invalid timestamps |
| Server Load Generator | Simulation | Hard | QPS, seed, duration, service times | Request schedule and compliance stats | Reproducible arrivals, correct queue timing, no dropped accounting |
| Benchmark Compliance Checker | Validation | Medium | Results, latency/quality rules | Pass/fail and violations | Exact threshold behavior and complete evidence |

## Visual teaching plan

- Animated request arrivals, queueing, execution, and completion for each scenario.
- Linked latency histogram and percentile markers that update when batching changes.
- Throughput-versus-latency frontier with the quality-compliant region shaded.
- Audit bundle explorer showing configuration, hashes, measurements, and rejected runs.

## MLOps and deployment extensions

Add deadline-miss rate, jitter, sustained thermal behavior, sensor-to-command latency, power draw, and safety fallback time. Report distributions per robot hardware revision rather than only an aggregate.

## Canonical sources

- [arXiv landing page](https://arxiv.org/abs/1911.02549)
- [arXiv PDF](https://arxiv.org/pdf/1911.02549)

