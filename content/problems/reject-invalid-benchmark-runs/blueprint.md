---
{
  "schema_version": 1,
  "problem_id": "reject-invalid-benchmark-runs",
  "content_version": "1.0.0",
  "status": "implemented",
  "title": "Reject Invalid Benchmark Runs",
  "summary": "Reject supplied benchmark evidence that has missing work, failures, inadequate coverage or mismatched run identity.",
  "type": "function",
  "difficulty": "medium",
  "estimated_minutes": 30,
  "domains": [
    "robotics-mlops"
  ],
  "topics": [
    "benchmark-validity",
    "quality-gates",
    "reproducibility"
  ],
  "paper_ids": [
    "2019-mlperf-inference"
  ],
  "paper_sections": [
    "Sections4.4,4.6,4.7 and5: quality, validity and review; supplied thresholds are original"
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
    "budget_status": "actual shared worker limits; isolated Run/Submit verified"
  },
  "entrypoint": "solution.benchmark_run_rejections",
  "physical_contract": "Counts are query counts; duration is integer nanoseconds on one declared benchmark interval. Quality is a caller-defined dimensionless score in[0,1]. No timing or accuracy measurements are collected by this function.",
  "grading": {
    "mode": "exact",
    "seed": 20261113,
    "rtol": 0,
    "atol": 0,
    "public_case_families": [
      "matching run at exact thresholds",
      "multiple independent rejection reasons",
      "wrong model and scenario"
    ],
    "hidden_case_families": [
      "completed/failed/requested accounting",
      "typed metadata and full schema",
      "empty evidence counters and threshold bounds",
      "deterministic reasons and preserved inputs"
    ],
    "performance_class": "none; no timing leaderboard",
    "evaluator_sha256": "8b1771d6a8ffed26c505013b26ad87d731aac8c1669b17209a5d3d8238de7891"
  },
  "fixtures": {
    "source": "original synthetic examples",
    "license": "CC0-1.0",
    "version_or_hash": "mlops-batch5-draft-0.1.0",
    "evaluator_sha256": null
  },
  "provenance": {
    "authoring_notes": "MLPerf motivates comparable workloads and valid quality-constrained measurements. This small evidence validator and its supplied thresholds are original; it is not an official MLPerf submission, statistical confidence or audit checker.",
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
  "reviewers": [
    "perception_completion"
  ]
}
---

# Reject Invalid Benchmark Runs

## Learning objective

Reject supplied benchmark evidence that has missing work, failures, inadequate coverage or mismatched run identity.

## Source and scope

MLPerf motivates comparable workloads and valid quality-constrained measurements. This small evidence validator and its supplied thresholds are original; it is not an official MLPerf submission, statistical confidence or audit checker. Source location: Sections4.4,4.6,4.7 and5: quality, validity and review; supplied thresholds are original. [Primary source](https://arxiv.org/html/1911.02549v1).

## Contract and examples

The normative typed contract is in statement.md; it includes the two worked examples expanded in examples.md. Inputs remain unchanged. This reviewed-before-code draft has no published meta.json.

## Implementation plan

Validate bounded run/protocol metadata and accounting; evaluate seven independent conditions; return sorted reasons. Constant work for fixed schemas.

## Evaluator plan

Public cases: matching run at exact thresholds; multiple independent rejection reasons; wrong model and scenario. Hidden cases: completed/failed/requested accounting; typed metadata and full schema; empty evidence counters and threshold bounds; deterministic reasons and preserved inputs. Check exact output structure/order/types, documented errors, bounds and input preservation. Generated data uses seed20261113. Before publication, implement starter/reference/cases, hash fixtures, independently review them, and run Run/Submit through the actual isolated baseline. Dependency setup failures are platform errors.

## Theory and visual

Original equations, worked traces, text alternatives, robot failure modes and questions are in theory.md. Static tables need no motion setting. hints.md reveals ideas progressively; review.md records answer keys and review status.

## Operations

Record content, inputs, configuration, runtime and evaluator versions with future scores. The source PDFs remain local research references; fixtures are original CC0-1.0. No remote service, simulator or dataset download is required.

