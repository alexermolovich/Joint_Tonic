---
{
  "schema_version": 1,
  "problem_id": "verify-immutable-run-manifest",
  "content_version": "1.0.0",
  "status": "implemented",
  "title": "Reproduce a Model from an Immutable Run Manifest",
  "summary": "Verify the exact artifact bytes, runtime identities and seed required before a declared model run can be replayed.",
  "type": "function",
  "difficulty": "medium",
  "estimated_minutes": 30,
  "domains": [
    "robotics-mlops"
  ],
  "topics": [
    "reproducible-runs",
    "artifact-verification"
  ],
  "paper_ids": [
    "2017-tfx-production-ml-platform"
  ],
  "paper_sections": [
    "Section2.2 pipeline integration; Section3 data/transform/model stages"
  ],
  "track_ids": [],
  "prerequisite_problem_ids": [
    "record-artifact-lineage"
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
  "entrypoint": "solution.verify_run_manifest",
  "physical_contract": {
    "frames": [],
    "units": {
      "seed": "dimensionless unsigned32 integer",
      "bytes": "binary artifact payloads",
      "sha256": "lowercase hexadecimal digest"
    },
    "axes": "Artifact names and environment names are metadata keys; no spatial axes.",
    "timestamp_assumptions": "Immutable run inputs; no wall clock or freshness inference.",
    "batching": "One manifest and one observed replay environment per call."
  },
  "grading": {
    "mode": "exact",
    "seed": 20261113,
    "rtol": 0,
    "atol": 0,
    "public_case_families": [
      "matching bytes and configuration",
      "mismatches and unexpected artifact"
    ],
    "hidden_case_families": [
      "missing versus mismatched values",
      "unexpected environment",
      "empty bytes",
      "malformed digest/versions",
      "seed mismatch",
      "byte-budget bound",
      "input preservation"
    ],
    "performance_class": "none; no timing leaderboard",
    "evaluator_sha256": "5872082a4415ef0f298e6a89efa8597c0d01ba0f0e3e61439826c23d86af516e"
  },
  "fixtures": {
    "source": "original synthetic examples",
    "license": "CC0-1.0",
    "version_or_hash": "sha256:5872082a4415ef0f298e6a89efa8597c0d01ba0f0e3e61439826c23d86af516e",
    "evaluator_sha256": "5872082a4415ef0f298e6a89efa8597c0d01ba0f0e3e61439826c23d86af516e",
    "generated_fixture_hash": "5872082a4415ef0f298e6a89efa8597c0d01ba0f0e3e61439826c23d86af516e"
  },
  "provenance": {
    "authoring_notes": "This is a bounded preflight component of model reproduction, motivated by TFX pipeline integration. It validates supplied bytes/versions/seed and deliberately does not run training or promise bitwise-identical weights. The manifest schema and rejection vocabulary are original.",
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

# Reproduce a Model from an Immutable Run Manifest

## Learning objective

Verify the exact artifact bytes, runtime identities and seed required before a declared model run can be replayed.

## Source and scope

This is a bounded preflight component of model reproduction, motivated by TFX pipeline integration. It validates supplied bytes/versions/seed and deliberately does not run training or promise bitwise-identical weights. The manifest schema and rejection vocabulary are original. Source location: Section2.2 pipeline integration; Section3 data/transform/model stages. [Primary source](https://research.google/pubs/tfx-a-tensorflow-based-production-scale-machine-learning-platform/).

## Contract and examples

The normative typed contract is in statement.md; it includes the two worked examples expanded in examples.md. Inputs remain unchanged. Version1.0.0 implements the reviewed0.1.0 contract; application metadata and evaluator are included.

## Implementation plan

Validate bounded mappings and payload lengths, use hashlib.sha256 for common artifacts, report set differences and mismatched values. O(total bytes+N log N) time with bounded O(N) metadata/output; no payload copies or external access.

## Evaluator plan

Public cases: matching bytes and configuration; mismatches and unexpected artifact. Hidden cases: missing versus mismatched values; unexpected environment; empty bytes; malformed digest/versions; seed mismatch; byte-budget bound; input preservation. Check exact output structure/order/types, documented errors, bounds and input preservation. Generated data uses seed20261113. Starter, reference, public/hidden cases and hashes are present. The reference passed actual isolated Run/Submit checks; independent implementation review is recorded in review.md. Dependency setup failures are platform errors.

## Theory and visual

Original equations, worked traces, text alternatives, robot failure modes and questions are in theory.md. Static tables need no motion setting. hints.md reveals ideas progressively; review.md records answer keys and review status.

## Operations

Record content, inputs, configuration, runtime and evaluator versions with future scores. The source PDFs remain local research references; fixtures are original CC0-1.0. No remote service, simulator or dataset download is required.
