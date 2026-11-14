---
{
  "schema_version": 1,
  "problem_id": "map-shared-robot-episode",
  "content_version": "1.0.0",
  "status": "implemented",
  "title": "Map Robot-Specific Data into a Shared Episode Schema",
  "summary": "Reorder scalar robot channels, perform declared compatible unit conversions and retain episode provenance.",
  "type": "function",
  "difficulty": "medium",
  "estimated_minutes": 30,
  "domains": [
    "robotics-mlops"
  ],
  "topics": [
    "cross-embodiment",
    "episode-schema",
    "units"
  ],
  "paper_ids": [
    "2024-open-x-embodiment"
  ],
  "paper_sections": [
    "SectionIV-A data format consolidation"
  ],
  "track_ids": [],
  "prerequisite_problem_ids": [],
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
    "solution_dependencies": [
      "numpy"
    ]
  },
  "entrypoint": "solution.remap_robot_episode",
  "physical_contract": "One episode of timestamped scalar position/delta channels. Clock timestamps are integer nanoseconds; samples share the declared frame. Length units m/cm/mm, angular units rad/deg and unitless scalars are supported. No frame, absolute/delta, robot-kinematic or velocity conversion is performed.",
  "grading": {
    "mode": "numerical",
    "seed": 20261113,
    "rtol": 1e-12,
    "atol": 1e-12,
    "public_case_families": [
      "reorder and centimetres-to-metres conversion",
      "degrees-to-radians and preserved metadata",
      "empty episode"
    ],
    "hidden_case_families": [
      "unit-family mismatch and unknown channels",
      "exact timestamps and copied storage",
      "dtype/range/metadata bounds",
      "noncontiguous signals and angle tolerance"
    ],
    "performance_class": "none; no timing leaderboard",
    "evaluator_sha256": "6a4d980c660c0d83faf0cc098a529068fcb22fbc1a578239fab06be8f37c6a9f"
  },
  "fixtures": {
    "source": "original synthetic examples",
    "license": "CC0-1.0",
    "version_or_hash": "sha256:6a4d980c660c0d83faf0cc098a529068fcb22fbc1a578239fab06be8f37c6a9f",
    "evaluator_sha256": "6a4d980c660c0d83faf0cc098a529068fcb22fbc1a578239fab06be8f37c6a9f",
    "generated_fixture_hash": "6a4d980c660c0d83faf0cc098a529068fcb22fbc1a578239fab06be8f37c6a9f"
  },
  "provenance": {
    "authoring_notes": "Open X-Embodiment motivates shared data interfaces that preserve robot-specific meaning. This restricted scalar position/delta mapper and unit table are original teaching choices; they do not reproduce every source dataset transform or make embodiments interchangeable.",
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
  "reviewers": [
    "perception_implementation"
  ],
  "derived_draft_version": "0.1.0"
}
---

# Map Robot-Specific Data into a Shared Episode Schema

## Learning objective

Reorder scalar robot channels, perform declared compatible unit conversions and retain episode provenance.

## Source and scope

Open X-Embodiment motivates shared data interfaces that preserve robot-specific meaning. This restricted scalar position/delta mapper and unit table are original teaching choices; they do not reproduce every source dataset transform or make embodiments interchangeable. Source location: SectionIV-A data format consolidation. [Primary source](https://arxiv.org/abs/2310.08864).

## Contract and examples

The normative typed contract is in statement.md; it includes the two worked examples expanded in examples.md. Inputs remain unchanged. Version1.0.0 implements the reviewed0.1.0 contract; application metadata and evaluator are included.

## Implementation plan

Validate exact episode fields and channel descriptors; construct a source lookup and compatible unit scales; copy/reorder converted columns with independent output arrays and metadata. O(TD+S), bounded by T<=10000,D<=64.

## Evaluator plan

Public cases: reorder and centimetres-to-metres conversion; degrees-to-radians and preserved metadata; empty episode. Hidden cases: unit-family mismatch and unknown channels; exact timestamps and copied storage; dtype/range/metadata bounds; noncontiguous signals and angle tolerance. Check exact output structure/order/types, documented errors, bounds and input preservation. Generated data uses seed20261113. Starter, reference, public/hidden cases and hashes are present. The reference passed actual isolated Run/Submit checks; independent implementation review is recorded in review.md. Dependency setup failures are platform errors.

## Theory and visual

Original equations, worked traces, text alternatives, robot failure modes and questions are in theory.md. Static tables need no motion setting. hints.md reveals ideas progressively; review.md records answer keys and review status.

## Operations

Record content, inputs, configuration, runtime and evaluator versions with future scores. The source PDFs remain local research references; fixtures are original CC0-1.0. No remote service, simulator or dataset download is required.

