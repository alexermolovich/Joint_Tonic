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
execution_flow: {"title":"Core execution flow","description":"Declare a robotics workload, correlate trace events through the graph, and compare quality-constrained timing on identified hardware.","nodes":[{"id":"stage-1","title":"Declare workload boundaries","detail":"Specify inputs, outputs, graph stages, rates, and measurement scope.","column":0,"row":0,"section":"Declare workload boundaries","problem_slugs":[],"planned_problems":["Declare Reproducible Robotics Benchmark Boundaries"]},{"id":"stage-2","title":"Analyze the timed graph","detail":"Separate processing time, waiting, transfer, and parallel work.","column":1,"row":0,"section":"Analyze the timed graph","problem_slugs":["inference-latency-percentiles"],"planned_problems":["Derive End-to-End Latency from Robotics Trace Events","Measure Throughput and Jitter Across a ROS-Style Graph"]},{"id":"stage-3","title":"Compare valid runs","detail":"Report distributions and configuration identity rather than a context-free speed number.","column":2,"row":0,"section":"Compare valid runs","problem_slugs":["edge-inference-release-gate"],"planned_problems":["Compare Black-Box and Grey-Box Pipeline Measurements"]}],"edges":[{"from":"stage-1","to":"stage-2","label":"correlated traces"},{"from":"stage-2","to":"stage-3","label":"timing distributions"}]}
---

## Core paper explanation

RobotPerf studies benchmarking of robotics computation across hardware platforms with explicit workloads and measurement methodology. It distinguishes black-box end-to-end observations from instrumentation that exposes component-level timing. The important educational boundary is reconstructing a timed computation graph without conflating sensor frequency, throughput, and latency.

## Execution flow

Declare a robotics workload, correlate trace events through the graph, and compare quality-constrained timing on identified hardware.

### Declare workload boundaries

For input event $i$ at time $t_i^{\mathrm{in}}$ and its associated output at $t_i^{\mathrm{out}}$,

$$
L_i=t_i^{\mathrm{out}}-t_i^{\mathrm{in}}.
$$

Both timestamps must share a clock or an explicit synchronization correction. Correlation IDs should link the same work item across stages; pairing outputs with the nearest input timestamp can mismeasure buffered pipelines.


**Component practice**

- Declare Reproducible Robotics Benchmark Boundaries — unreviewed idea; contract and evaluator required.

### Analyze the timed graph

For a strictly serial path $P$, end-to-end latency is the sum of service and waiting times:

$$
L_P=\sum_{v\in P}(S_v+W_v).
$$

Parallel graphs require critical-path reasoning rather than summing every event duration. Instrumentation can change timing, so document probe overhead and compare grey-box measurements with the external workload boundary.


**Component practice**

- Supporting prerequisite: [Compute p50, p90, and p99 Inference Latency](/problems/inference-latency-percentiles). Practices the stated data or mathematical operation; it does not implement this paper-specific stage in full.
- Derive End-to-End Latency from Robotics Trace Events — unreviewed idea; contract and evaluator required.
- Measure Throughput and Jitter Across a ROS-Style Graph — unreviewed idea; contract and evaluator required.

### Compare valid runs

Throughput is completed work divided by observation time; latency is time per correlated work item. A pipeline can improve throughput while worsening tail latency. [Edge model release gating](/problems/edge-inference-release-gate) provides related practice with explicit quality and latency records. Benchmark results also require workload, device, driver, runtime, and measurement-mode identity.


**Component practice**

- Supporting prerequisite: [Gate an Edge Model with Accuracy and Latency](/problems/edge-inference-release-gate). Practices the stated data or mathematical operation; it does not implement this paper-specific stage in full.
- Compare Black-Box and Grey-Box Pipeline Measurements — unreviewed idea; contract and evaluator required.

## Implement the components

Each execution-flow node links the matching runnable component or names its planned problem. Planned titles are not runnable; labels distinguish reviewed drafts from unreviewed ideas.

- **Supporting prerequisite:** [Compute p50, p90, and p99 Inference Latency](/problems/inference-latency-percentiles).
- **Supporting prerequisite:** [Gate an Edge Model with Accuracy and Latency](/problems/edge-inference-release-gate).

**Planned component problems:**

- Declare Reproducible Robotics Benchmark Boundaries — unreviewed idea; contract and evaluator required.
- Derive End-to-End Latency from Robotics Trace Events — unreviewed idea; contract and evaluator required.
- Measure Throughput and Jitter Across a ROS-Style Graph — unreviewed idea; contract and evaluator required.
- Compare Black-Box and Grey-Box Pipeline Measurements — unreviewed idea; contract and evaluator required.

These bounded exercises do not claim to reproduce the complete paper or its benchmark results.

## Why this matters on a robot

Robotics graphs include sensors, middleware, transfers, accelerators, and controllers. Measuring one kernel can miss the bottleneck that delays an actual command. Trace loss, clock mismatch, and dropped messages must be reported rather than silently discarded.

## Sources and scope

[Primary paper](https://arxiv.org/abs/2309.09212) · [Open-access manuscript](https://arxiv.org/pdf/2309.09212)

This is an original explanation of selected mechanisms. Equations use the notation defined here; simplified teaching models are identified explicitly. Small component exercises do not reproduce the paper's full experiments. The local PDF is a research reference; its redistribution terms remain those recorded in the metadata.
