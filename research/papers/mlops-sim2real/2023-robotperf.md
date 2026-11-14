---
schema_version: 1
paper_id: "2023-robotperf"
title: "RobotPerf: An Open-Source, Vendor-Agnostic, Benchmarking Suite for Evaluating Robotics Computing System Performance"
authors:
  - "Victor Mayoral-Vilches et al."
year: 2023
venue_or_status: "arXiv 2023; open benchmark suite"
primary_url: "https://arxiv.org/abs/2309.09212"
pdf_url: "https://arxiv.org/pdf/2309.09212"
local_pdf: "./2023-robotperf.pdf"
sha256: "fd61fd4331f547382bcc0063221c13f11c8c6953848c95eab1249e6ca71418b9"
bytes: 2271155
pages: 9
topics:
  - "robotics-benchmarking"
  - "ros2"
  - "tracing"
  - "latency"
  - "hardware-acceleration"
modalities:
  - "ros2-events"
  - "computation-graphs"
  - "timing-traces"
  - "power-metrics"
track_role: "supporting"
open_access_status: "open-access-preprint"
redistribution_note: "Research copy only; verify the source license before redistribution."
---

## Agent brief

Implement trace analysis for a ROS-style computation graph. Distinguish black-box end-to-end measurement from grey-box instrumentation that reveals component bottlenecks.

## Contribution

RobotPerf provides vendor-neutral robotics benchmarks around ROS 2 and spans perception, localization, control, and related workloads. It formalizes black-box and grey-box approaches for comparable compute-system measurements.

## Prerequisite concepts

- Distributed timestamps and trace events
- Directed robotics computation graphs
- Latency, throughput, jitter, and power metrics
- ROS 2 concepts are helpful but not required

## Essential theory

For a correlated message path, black-box end-to-end latency is

$$
L_{\mathrm{e2e}}=t_{\mathrm{output}}-t_{\mathrm{input}}.
$$

Grey-box spans decompose this interval into node execution, transport, queueing, and idle gaps. On a dependency DAG, the critical path is the path with maximum accumulated duration, not necessarily the sum of all node times.

## Method map

| Component | Input | Output | Core invariant | Good exercise boundary |
| --- | --- | --- | --- | --- |
| Trace correlator | Out-of-order ROS-style events | Complete spans and rejected records | Each accepted span has one unambiguous causal identity | Correlate one message path |
| Metric aggregator | Correlated spans | Latency, jitter, throughput, and deadline metrics | Units and percentile conventions are explicit | Summarize one workload run |
| Critical-path analyzer | Dependency DAG and node/transport durations | Critical path and slack | Only causally valid DAG paths are compared | Compute longest path for one trace graph |

- Standardized robotics workloads
- ROS 2 graph as a common integration layer
- Black-box input/output timing
- Grey-box internal event tracing
- Reproducible hardware/software metadata
- Cross-platform result comparison

## Data and evaluation

Provide synthetic traces for camera, preprocessing, detector, planner, and controller nodes, including concurrency and missing events. Grade correlation, critical-path latency, throughput, jitter, and handling of malformed traces.

## Limitations and failure modes

Instrumentation can perturb the system, and results are only comparable under aligned workload definitions. Synthetic traces do not capture scheduling, thermal, network, or real-time operating-system effects.

## Implementation decomposition

1. Parse normalized send, receive, start, and finish events.
2. Correlate messages across nodes and reject ambiguous spans.
3. Compute node and end-to-end statistics.
4. Identify the critical path and bottleneck contributions.
5. Attach complete hardware/software provenance.

## Problem blueprints

| Title | Type | Difficulty | Inputs | Outputs | Grading |
| --- | --- | --- | --- | --- | --- |
| Correlate Robotics Traces | Data processing | Hard | Out-of-order events with IDs | Complete spans and rejected records | Exact correlation, duplicate/missing-event handling |
| End-to-End Latency and Jitter | Metrics | Medium | Completed spans | Distribution and jitter metrics | Units, percentile convention, stable grouping |
| Critical Path in a ROS Graph | Graph algorithm | Hard | Node durations and dependencies | Critical path and slack | Correct longest path on DAG, clear cycle failure |

## Visual teaching plan

- Toggle between black-box input/output timing and grey-box internal spans.
- Gantt chart of correlated messages across perception, planning, and control nodes.
- Critical-path overlay on the robotics computation graph.
- Hardware comparison dashboard for latency, jitter, throughput, power, and deadline misses.

## MLOps and deployment extensions

Run benchmarks in CI on representative robot SKUs and after firmware, driver, model, or compiler changes. Gate releases on deadline misses and per-stage regressions, not only mean latency.

## Canonical sources

- [arXiv landing page](https://arxiv.org/abs/2309.09212)
- [arXiv PDF](https://arxiv.org/pdf/2309.09212)

