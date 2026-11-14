---
{
  "schema_version": 1,
  "problem_id": "record-artifact-lineage",
  "content_version": "1.0.0",
  "status": "implemented",
  "title": "Record Dataset, Transform, Model, and Evaluator Lineage",
  "summary": "Build a dependency-complete provenance record for one artifact while preserving the identity of every upstream input.",
  "type": "function",
  "difficulty": "medium",
  "estimated_minutes": 30,
  "domains": [
    "robotics-mlops"
  ],
  "topics": [
    "artifact-lineage",
    "reproducibility"
  ],
  "paper_ids": [
    "2017-tfx-production-ml-platform"
  ],
  "paper_sections": [
    "Section2.2: platform design and pipeline anatomy"
  ],
  "track_ids": [],
  "prerequisite_problem_ids": [
    "training-pipeline-topological-order"
  ],
  "runtime": {
    "language": "python",
    "python": "3.12.3",
    "runtime_id": "python-3.12.3-numpy-2.2.4-torch-2.6.0-cpu-bwrap-v2",
    "image_digest": null,
    "image_status": "pending OCI build; actual local bubblewrap Run and Submit verified",
    "dependencies": {
      "numpy": "2.2.4",
      "torch": "2.6.0+cpu"
    },
    "platform": "linux-x86_64-cpu",
    "limits": {
      "wall_seconds": 18,
      "cpu_seconds": 10,
      "memory_mb": 4096,
      "output_kb": 64
    },
    "budget_status": "actual shared worker caps; per-process address-space limit",
    "solution_dependencies": []
  },
  "entrypoint": "solution.lineage_record",
  "physical_contract": {
    "frames": [],
    "units": {
      "sha256": "64-character lowercase hexadecimal identity",
      "ids": "dimensionless artifact IDs"
    },
    "axes": "parents[consumer] lists its direct producer/input IDs.",
    "timestamp_assumptions": "One immutable artifact snapshot; no chronological ordering inferred from IDs.",
    "batching": "One target artifact per graph call."
  },
  "grading": {
    "mode": "exact",
    "seed": 20261113,
    "rtol": 0,
    "atol": 0,
    "public_case_families": [
      "dataset-transform-model-evaluator chain",
      "shared parent and isolated artifact"
    ],
    "hidden_case_families": [
      "duplicate parents",
      "different IDs with same digest",
      "full-graph cycle errors",
      "unknown IDs",
      "long DAG",
      "nonmutation"
    ],
    "performance_class": "none; no timing leaderboard",
    "evaluator_sha256": "929338f5ec4c733da11f0113e92be031f6fad5dfc1ab0861edde7152f9568640"
  },
  "fixtures": {
    "source": "original synthetic examples",
    "license": "CC0-1.0",
    "version_or_hash": "sha256:929338f5ec4c733da11f0113e92be031f6fad5dfc1ab0861edde7152f9568640",
    "evaluator_sha256": "929338f5ec4c733da11f0113e92be031f6fad5dfc1ab0861edde7152f9568640",
    "generated_fixture_hash": "929338f5ec4c733da11f0113e92be031f6fad5dfc1ab0861edde7152f9568640"
  },
  "provenance": {
    "authoring_notes": "TFX motivates coordinating versioned pipeline artifacts. The graph schema and returned ancestry record are original teaching choices, not a universal TFX metadata API. Supplied digests are recorded but not verified against bytes in this component.",
    "primary_urls": [
      "https://research.google/pubs/tfx-a-tensorflow-based-production-scale-machine-learning-platform/"
    ],
    "implementation_urls": [],
    "paper_card": "research/papers/mlops-sim2real/2017-tfx-production-ml-platform.md",
    "manifest": "research/manifests/mlops-sim2real.md"
  },
  "owners": [
    "code_issue_scout"
  ],
  "reviewers": [
    "perception_implementation"
  ],
  "derived_draft_version": "0.1.0"
}
---

# Record Dataset, Transform, Model, and Evaluator Lineage

## Learning objective

Build a dependency-complete provenance record for one artifact while preserving the identity of every upstream input.

## Source and scope

TFX motivates coordinating versioned pipeline artifacts. The graph schema and returned ancestry record are original teaching choices, not a universal TFX metadata API. Supplied digests are recorded but not verified against bytes in this component. Source location: Section2.2: platform design and pipeline anatomy. [Primary source](https://research.google/pubs/tfx-a-tensorflow-based-production-scale-machine-learning-platform/).

## Contract and examples

The normative typed contract is in statement.md; it includes the two worked examples expanded in examples.md. Inputs remain unchanged. Version1.0.0 implements the reviewed0.1.0 contract; application metadata and evaluator are included.

## Implementation plan

Validate the DAG using a Kahn queue, then traverse target parents iteratively. O(V+E+V log V) time including output sort; O(V+E) memory. No filesystem or artifact loader.

## Evaluator plan

Public cases: dataset-transform-model-evaluator chain; shared parent and isolated artifact. Hidden cases: duplicate parents; different IDs with same digest; full-graph cycle errors; unknown IDs; long DAG; nonmutation. Check exact output structure/order/types, documented errors, bounds and input preservation. Generated data uses seed20261113. Starter, reference, public/hidden cases and hashes are present. The reference passed actual isolated Run/Submit checks; independent implementation review is recorded in review.md. Dependency setup failures are platform errors.

## Theory and visual

Original equations, worked traces, text alternatives, robot failure modes and questions are in theory.md. Static tables need no motion setting. hints.md reveals ideas progressively; review.md records answer keys and review status.

## Operations

Record content, inputs, configuration, runtime and evaluator versions with future scores. The source PDFs remain local research references; fixtures are original CC0-1.0. No remote service, simulator or dataset download is required.
