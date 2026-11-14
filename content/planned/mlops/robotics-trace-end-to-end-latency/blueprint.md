---
{
  "schema_version": 1,
  "problem_id": "robotics-trace-end-to-end-latency",
  "content_version": "0.1.0",
  "status": "drafted",
  "title": "Derive End-to-End Latency from Robotics Trace Events",
  "summary": "Pair boundary events by request identity and compute exact end-to-end latency on one declared clock.",
  "type": "function",
  "difficulty": "medium",
  "estimated_minutes": 30,
  "domains": [
    "robotics-mlops"
  ],
  "topics": [
    "robotics-tracing",
    "correlation-ids",
    "end-to-end-latency"
  ],
  "paper_ids": [
    "2023-robotperf"
  ],
  "paper_sections": [
    "SectionIII-D methodology and III-G metrics"
  ],
  "track_ids": [],
  "prerequisite_problem_ids": [],
  "runtime": {
    "language": "python",
    "python": "3.12.3",
    "runtime_id": "python-3.12.3-numpy-2.2.4-torch-2.6.0-cpu-bwrap-v2",
    "image_digest": null,
    "image_status": "pending OCI build; baseline worker exists",
    "dependencies": {},
    "platform": "linux-x86_64-cpu",
    "limits": {
      "wall_seconds": 18,
      "cpu_seconds": 10,
      "memory_mb": 4096,
      "output_kb": 64
    },
    "budget_status": "actual shared worker limits; this draft has not run"
  },
  "entrypoint": "solution.trace_latencies",
  "physical_contract": "Events use integer nanoseconds from one shared monotonic clock ID. Each request has one input and one output boundary. No clock correction, stage-duration summation, nearest-time pairing or robot actuation is performed.",
  "grading": {
    "mode": "exact",
    "seed": 20261113,
    "rtol": 0,
    "atol": 0,
    "public_case_families": [
      "out-of-order trace events with correct IDs",
      "large clock origin and zero latency",
      "empty trace"
    ],
    "hidden_case_families": [
      "duplicate/missing boundaries rejected",
      "different clocks and reverse time rejected",
      "typed event limits and IDs",
      "sorted results and preservation at scale"
    ],
    "performance_class": "none; no timing leaderboard"
  },
  "fixtures": {
    "source": "original synthetic examples",
    "license": "CC0-1.0",
    "version_or_hash": "mlops-batch5-draft-0.1.0",
    "evaluator_sha256": null
  },
  "provenance": {
    "authoring_notes": "RobotPerf motivates explicit workload boundaries and correlated timing. The strict two-event schema is an original bounded trace-analysis exercise, not a complete ROS trace parser or critical-path reconstruction.",
    "primary_urls": [
      "https://arxiv.org/html/2309.09212v2"
    ],
    "implementation_urls": [],
    "paper_card": "research/papers/mlops-sim2real/2023-robotperf.md",
    "manifest": "research/manifests/mlops-sim2real.md"
  },
  "owners": [
    "code_issue_scout"
  ],
  "reviewers": []
}
---

# Derive End-to-End Latency from Robotics Trace Events

## Learning objective

Pair boundary events by request identity and compute exact end-to-end latency on one declared clock.

## Source and scope

RobotPerf motivates explicit workload boundaries and correlated timing. The strict two-event schema is an original bounded trace-analysis exercise, not a complete ROS trace parser or critical-path reconstruction. Source location: SectionIII-D methodology and III-G metrics. [Primary source](https://arxiv.org/html/2309.09212v2).

## Contract and examples

The normative typed contract is in statement.md; it includes the two worked examples expanded in examples.md. Inputs remain unchanged. This reviewed-before-code draft has no published meta.json.

## Implementation plan

Validate and index up to200000 events; require exact complete pairs; subtract correlated timestamps and return sorted IDs. O(N+RlogR) time and O(R) storage for R requests.

## Evaluator plan

Public cases: out-of-order trace events with correct IDs; large clock origin and zero latency; empty trace. Hidden cases: duplicate/missing boundaries rejected; different clocks and reverse time rejected; typed event limits and IDs; sorted results and preservation at scale. Check exact output structure/order/types, documented errors, bounds and input preservation. Generated data uses seed20261113. Before publication, implement starter/reference/cases, hash fixtures, independently review them, and run Run/Submit through the actual isolated baseline. Dependency setup failures are platform errors.

## Theory and visual

Original equations, worked traces, text alternatives, robot failure modes and questions are in theory.md. Static tables need no motion setting. hints.md reveals ideas progressively; review.md records answer keys and review status.

## Operations

Record content, inputs, configuration, runtime and evaluator versions with future scores. The source PDFs remain local research references; fixtures are original CC0-1.0. No remote service, simulator or dataset download is required.

