---
{
  "schema_version": 1,
  "problem_id": "infer-robot-episode-schema",
  "content_version": "1.0.0",
  "status": "implemented",
  "title": "Infer a Schema from Robot Episodes",
  "summary": "Propose signal shapes, metadata and per-channel observed ranges from a bounded collection of robot episodes.",
  "type": "function",
  "difficulty": "medium",
  "estimated_minutes": 30,
  "domains": [
    "robotics-mlops"
  ],
  "topics": [
    "schema-inference",
    "robot-data"
  ],
  "paper_ids": [
    "2019-data-validation-for-ml"
  ],
  "paper_sections": [
    "Sections3–4: schema-based validation and schema inference"
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
  "entrypoint": "solution.infer_episode_schema",
  "physical_contract": {
    "frames": [
      "Explicit frame string carried by each signal"
    ],
    "units": {
      "values": "Explicit common unit string per signal; never inferred from numbers",
      "minimum": "Same unit and frame as the corresponding channel",
      "maximum": "Same unit and frame as the corresponding channel"
    },
    "axes": "values(T,D): rows are recorded samples, columns are fixed signal channels.",
    "timestamp_assumptions": "Episode order and sample frequency are not inferred. Each signal is already aligned under its declared metadata.",
    "batching": "A list of independent episodes; missing signals are allowed and change required status."
  },
  "grading": {
    "mode": "numerical",
    "seed": 20261113,
    "rtol": 0,
    "atol": 0,
    "public_case_families": [
      "two episodes with optional signal",
      "empty collection"
    ],
    "hidden_case_families": [
      "per-channel extrema",
      "varying sample counts",
      "metadata/width conflicts",
      "noncontiguous float64 inputs",
      "invalid/missing record fields",
      "total scalar bound",
      "independent output arrays"
    ],
    "performance_class": "none; no timing leaderboard",
    "evaluator_sha256": "b821c521282a0b10e6c254065c6801fb664d43da16b1990dd4dd3edb81c136cf"
  },
  "fixtures": {
    "source": "original synthetic examples",
    "license": "CC0-1.0",
    "version_or_hash": "sha256:b821c521282a0b10e6c254065c6801fb664d43da16b1990dd4dd3edb81c136cf",
    "evaluator_sha256": "b821c521282a0b10e6c254065c6801fb664d43da16b1990dd4dd3edb81c136cf",
    "generated_fixture_hash": "b821c521282a0b10e6c254065c6801fb664d43da16b1990dd4dd3edb81c136cf"
  },
  "provenance": {
    "authoring_notes": "The paper motivates proposing schemas from observed data and reviewing them before enforcement. This numeric robot-signal schema and range policy are original; observed extrema are not hardware limits or a guarantee about unseen data.",
    "primary_urls": [
      "https://research.google/pubs/data-validation-for-machine-learning/"
    ],
    "implementation_urls": [],
    "paper_card": "research/papers/mlops-sim2real/2019-data-validation-for-ml.md",
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

# Infer a Schema from Robot Episodes

## Learning objective

Propose signal shapes, metadata and per-channel observed ranges from a bounded collection of robot episodes.

## Source and scope

The paper motivates proposing schemas from observed data and reviewing them before enforcement. This numeric robot-signal schema and range policy are original; observed extrema are not hardware limits or a guarantee about unseen data. Source location: Sections3–4: schema-based validation and schema inference. [Primary source](https://research.google/pubs/data-validation-for-machine-learning/).

## Contract and examples

The normative typed contract is in statement.md; it includes the two worked examples expanded in examples.md. Inputs remain unchanged. Version1.0.0 implements the reviewed0.1.0 contract; application metadata and evaluator are included.

## Implementation plan

Validate each occurrence and accumulate channel minima/maxima plus presence counts without concatenating episodes. O(total input scalars) arithmetic and O(sum of signal widths) accumulator memory. Return fresh float64 range arrays.

## Evaluator plan

Public cases: two episodes with optional signal; empty collection. Hidden cases: per-channel extrema; varying sample counts; metadata/width conflicts; noncontiguous float64 inputs; invalid/missing record fields; total scalar bound; independent output arrays. Check exact output structure/order/types, documented errors, bounds and input preservation. Generated data uses seed20261113. Starter, reference, public/hidden cases and hashes are present. The reference passed actual isolated Run/Submit checks; independent implementation review is recorded in review.md. Dependency setup failures are platform errors.

## Theory and visual

Original equations, worked traces, text alternatives, robot failure modes and questions are in theory.md. Static tables need no motion setting. hints.md reveals ideas progressively; review.md records answer keys and review status.

## Operations

Record content, inputs, configuration, runtime and evaluator versions with future scores. The source PDFs remain local research references; fixtures are original CC0-1.0. No remote service, simulator or dataset download is required.
