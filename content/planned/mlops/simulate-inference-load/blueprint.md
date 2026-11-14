---
{
  "schema_version": 1,
  "problem_id": "simulate-inference-load",
  "content_version": "0.1.0",
  "status": "drafted",
  "title": "Simulate Single-Stream and Server Load",
  "summary": "Distinguish closed-loop query issuance from externally arriving requests and include queue waiting in latency.",
  "type": "function",
  "difficulty": "medium",
  "estimated_minutes": 30,
  "domains": [
    "robotics-mlops"
  ],
  "topics": [
    "inference-benchmarking",
    "queueing",
    "load-scenarios"
  ],
  "paper_ids": [
    "2019-mlperf-inference"
  ],
  "paper_sections": [
    "Section4.5 Scenarios and Metrics; Section4.7 Load Generator"
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
  "entrypoint": "solution.simulate_inference_load",
  "physical_contract": "All times are integer nanoseconds on one synthetic monotonic clock. One nonpreemptive server handles requests in input order. No physical robot, network, batching, GPU synchronization or wall-clock measurement is involved.",
  "grading": {
    "mode": "exact",
    "seed": 20261113,
    "rtol": 0,
    "atol": 0,
    "public_case_families": [
      "closed-loop single-stream issuance",
      "server backlog and waiting",
      "empty trace"
    ],
    "hidden_case_families": [
      "equal arrivals preserve request order",
      "idle gaps and exact large integer clock",
      "scenario-specific typed validation",
      "large deterministic workload"
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
    "authoring_notes": "The historical MLPerf2019 paper motivates scenario-dependent query issuance. The supplied-arrival, single-server FCFS recurrence is an original teaching simulator, not the official LoadGen or compliance protocol.",
    "primary_urls": [
      "https://arxiv.org/html/1911.02549v1"
    ],
    "implementation_urls": [],
    "paper_card": "research/papers/mlops-sim2real/2019-mlperf-inference.md",
    "manifest": "research/manifests/mlops-sim2real.md"
  },
  "owners": [
    "code_issue_scout"
  ],
  "reviewers": []
}
---

# Simulate Single-Stream and Server Load

## Learning objective

Distinguish closed-loop query issuance from externally arriving requests and include queue waiting in latency.

## Source and scope

The historical MLPerf2019 paper motivates scenario-dependent query issuance. The supplied-arrival, single-server FCFS recurrence is an original teaching simulator, not the official LoadGen or compliance protocol. Source location: Section4.5 Scenarios and Metrics; Section4.7 Load Generator. [Primary source](https://arxiv.org/html/1911.02549v1).

## Contract and examples

The normative typed contract is in statement.md; it includes the two worked examples expanded in examples.md. Inputs remain unchanged. This reviewed-before-code draft has no published meta.json.

## Implementation plan

Validate services/scenario/arrivals, then scan once with previous completion. O(N) time and O(N) returned schedule; no priority queue or simulator dependency.

## Evaluator plan

Public cases: closed-loop single-stream issuance; server backlog and waiting; empty trace. Hidden cases: equal arrivals preserve request order; idle gaps and exact large integer clock; scenario-specific typed validation; large deterministic workload. Check exact output structure/order/types, documented errors, bounds and input preservation. Generated data uses seed20261113. Before publication, implement starter/reference/cases, hash fixtures, independently review them, and run Run/Submit through the actual isolated baseline. Dependency setup failures are platform errors.

## Theory and visual

Original equations, worked traces, text alternatives, robot failure modes and questions are in theory.md. Static tables need no motion setting. hints.md reveals ideas progressively; review.md records answer keys and review status.

## Operations

Record content, inputs, configuration, runtime and evaluator versions with future scores. The source PDFs remain local research references; fixtures are original CC0-1.0. No remote service, simulator or dataset download is required.

