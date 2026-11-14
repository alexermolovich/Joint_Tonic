---
{
  "schema_version": 1,
  "problem_id": "per-embodiment-transfer-matrix",
  "content_version": "0.1.0",
  "status": "drafted",
  "title": "Build a Per-Embodiment Transfer Matrix",
  "summary": "Aggregate source-policy and target-robot evaluation evidence into a matrix while distinguishing unmeasured cells.",
  "type": "function",
  "difficulty": "medium",
  "estimated_minutes": 30,
  "domains": [
    "robotics-mlops"
  ],
  "topics": [
    "cross-embodiment",
    "transfer-evaluation"
  ],
  "paper_ids": [
    "2024-open-x-embodiment"
  ],
  "paper_sections": [
    "SectionIV data consolidation and SectionV cross-embodiment evaluation"
  ],
  "track_ids": [],
  "prerequisite_problem_ids": [],
  "runtime": {
    "language": "python",
    "python": "3.12.3",
    "runtime_id": "python-3.12.3-numpy-2.2.4-torch-2.6.0-cpu-bwrap-v2",
    "image_digest": null,
    "image_status": "pending OCI build; baseline worker exists",
    "dependencies": {
      "numpy": "2.2.4"
    },
    "platform": "linux-x86_64-cpu",
    "limits": {
      "wall_seconds": 18,
      "cpu_seconds": 10,
      "memory_mb": 4096,
      "output_kb": 64
    },
    "budget_status": "actual shared worker limits; this draft has not run"
  },
  "entrypoint": "solution.build_transfer_matrix",
  "physical_contract": "Input metadata defines each robot's channels and task protocol. The function preserves supplied meanings; no robot kinematics, coordinate conversion, clock alignment or hardware execution occurs.",
  "grading": {
    "mode": "numerical",
    "seed": 20261113,
    "rtol": 1e-12,
    "atol": 1e-12,
    "public_case_families": [
      "pooled trials in one source-target cell",
      "missing cell versus measured zero success",
      "empty evaluation"
    ],
    "hidden_case_families": [
      "axis order and repeated records",
      "exact integer counters and masks",
      "invalid labels/counters/unknown axes",
      "bounded scale and independent arrays"
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
    "authoring_notes": "Open X-Embodiment motivates preserving heterogeneous data meaning and reporting cross-embodiment results. This bounded deterministic interface is an original teaching decomposition, not the full RT-X model, dataset tooling or experimental protocol.",
    "primary_urls": [
      "https://arxiv.org/abs/2310.08864"
    ],
    "implementation_urls": [],
    "paper_card": "research/papers/mlops-sim2real/2024-open-x-embodiment.md",
    "manifest": "research/manifests/mlops-sim2real.md"
  },
  "owners": [
    "code_issue_scout"
  ],
  "reviewers": []
}
---

# Build a Per-Embodiment Transfer Matrix

## Learning objective

Aggregate source-policy and target-robot evaluation evidence into a matrix while distinguishing unmeasured cells.

## Source and scope

Open X-Embodiment motivates preserving heterogeneous data meaning and reporting cross-embodiment results. This bounded deterministic interface is an original teaching decomposition, not the full RT-X model, dataset tooling or experimental protocol. Source location: SectionIV data consolidation and SectionV cross-embodiment evaluation. [Primary source](https://arxiv.org/abs/2310.08864).

## Contract and examples

The normative typed contract is in statement.md; it includes the two worked examples expanded in examples.md. Inputs remain unchanged. This reviewed-before-code draft has no published meta.json.

## Implementation plan

Validate axis lists and records; sum counters in bounded S-by-T arrays; derive observed mask and conditional rates. O(N+ST) time and O(ST) output memory.

## Evaluator plan

Public cases: pooled trials in one source-target cell; missing cell versus measured zero success; empty evaluation. Hidden cases: axis order and repeated records; exact integer counters and masks; invalid labels/counters/unknown axes; bounded scale and independent arrays. Check exact output structure/order/types, documented errors, bounds and input preservation. Generated data uses seed20261113. Before publication, implement starter/reference/cases, hash fixtures, independently review them, and run Run/Submit through the actual isolated baseline. Dependency setup failures are platform errors.

## Theory and visual

Original equations, worked traces, text alternatives, robot failure modes and questions are in theory.md. Static tables need no motion setting. hints.md reveals ideas progressively; review.md records answer keys and review status.

## Operations

Record content, inputs, configuration, runtime and evaluator versions with future scores. The source PDFs remain local research references; fixtures are original CC0-1.0. No remote service, simulator or dataset download is required.

